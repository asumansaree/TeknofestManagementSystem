from tkinter import *
from tkinter import messagebox
from database_connection import *

mydb, cursor = initialize_connection()
#dropAllDB()
mydb.autocommit=False

class Main_App:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("500x400")  # Increased screen size (width x height)
        self.window.resizable(0, 0)
        self.window.config(background="#2596BE")  # Set the background color of the window
        self.window.title("TEKNOFEST MANAGEMENT SYSTEM")  # Window title

        # Define the button color and size
        button_bg_color = "#2596BE"  # Button background color
        button_fg_color = "#FFFFFF"  # Button text color (white)
        button_width = 56  # Button width (adjusted for larger window)
        button_height = 3  # Button height

        # Create and place the buttons with updated positions
        organizer_button = Button(
            self.window, text="Organizer Login", width=button_width, height=button_height, 
            command=Organizer_App, bg=button_bg_color, fg=button_fg_color
        )
        organizer_button.place(x=5, y=20)  # Adjusted position for larger window

        jury_button = Button(
            self.window, text="Jury Login", width=button_width, height=button_height, 
            command=Jury_App, bg=button_bg_color, fg=button_fg_color
        )
        jury_button.place(x=5, y=110)  # Adjusted position for larger window

        competitor_button = Button(
            self.window, text="Competitor Login", width=button_width, height=button_height, 
            command=Competitor_App, bg=button_bg_color, fg=button_fg_color
        )
        competitor_button.place(x=5, y=200)  # Adjusted position for larger window

        visitor_button = Button(
            self.window, text="Visitor Login", width=button_width, height=button_height, 
            command=Visitor_App, bg=button_bg_color, fg=button_fg_color
        )
        visitor_button.place(x=5, y=290)  # Adjusted position for larger window


class Organizer_App:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("1500x600")  # Screen Size(yatay x dikey)
        self.window.resizable(0, 0)
        self.window.columnconfigure(0, weight=1)
        self.window.config(background="#9BABB8")
        self.window.title("Organizer")  # Pencere ismi

        button_bg_color = "#2596BE" 
        button_fg_color = "#FFFFFF" 

        self.entries = []
        create_competition_button = Button(self.window, text="Create Competition",
                                    width=12, height=3, command=self.createCompetition, bg=button_bg_color, fg=button_fg_color)
        create_competition_button.place(x=2, y=5)
        view_competition_details_button = Button(self.window, text="Edit Competition",
                                    width=12, height=3, command=self.editCompetition, bg=button_bg_color, fg=button_fg_color)
        view_competition_details_button.place(x=142, y=5)
        edit_competition_details_button = Button(self.window, text="Cancel Competition",
                                           width=12, height=3, command=self.cancelCompetition, bg=button_bg_color, fg=button_fg_color)
        edit_competition_details_button.place(x=282, y=5)
        list_competition_button = Button(self.window, text="List Competitions",
                                   width=12, height=3, command=self.listCompetitions, bg=button_bg_color, fg=button_fg_color)
        list_competition_button.place(x=422, y=5)
        invite_jury_button = Button(self.window, text="List Juries",
                                    width=12, height=3 , command=self.listJuries, bg=button_bg_color, fg=button_fg_color)
        invite_jury_button.place(x=562, y=5)
        invite_jury_button = Button(self.window, text="List Venues",
                                       width=12, height=3, command=self.listVenues, bg=button_bg_color, fg=button_fg_color)
        invite_jury_button.place(x=702, y=5)
        invite_jury_button = Button(self.window, text="See Report",
                                       width=12, height=3, command=self.seeReport, bg=button_bg_color, fg=button_fg_color)
        invite_jury_button.place(x=842, y=5)
        invite_jury_button = Button(self.window, text="Add Report",
                                       width=12, height=3, command=self.addReport, bg=button_bg_color, fg=button_fg_color)
        invite_jury_button.place(x=982, y=5)
    
    def seeReport(self):
       eny = ReportDialog(0)
    def addReport(self):
       eny = ReportDialog(1)
       
    def cancelCompetition(self):
       eny = CancelCompetitionDialog(0)

    def listCompetitions(self):
        global cursor
        clearEntries(self.entries)
        cursor.execute("""SELECT * FROM Competition LEFT JOIN Venue ON Competition.venue_id = Venue.venue_id
                  UNION
                  SELECT * FROM Competition RIGHT JOIN Venue ON Competition.venue_id = Venue.venue_id
                  WHERE Competition.competition_id IS NOT NULL""")
        
        column_names = [desc[0] for desc in cursor.description]
        
        # Adjust the width to an even larger value for better visibility
        column_width = 40  # Significantly increase width to fit longer text
        
        # Display column names with the new width
        for j, column_name in enumerate(column_names):
            self.entries.append(Entry(self.window, width=column_width, fg='black'))
            self.entries[j].place(x=(120 * j), y=80)  # Adjust x position to ensure enough spacing
            self.entries[j].insert(END, column_name)
        
        i = 1
        for competition in cursor:
            for j in range(len(competition)):
                self.entries.append(Entry(self.window, width=column_width, fg='black'))
                self.entries[i * len(competition) + j].place(x=(120 * j), y=(25 * i) + 80)  # Adjust x position to ensure enough spacing
                self.entries[i * len(competition) + j].insert(END, str(competition[j]))
            i += 1


    def listVenues(self):
        global cursor
        clearEntries(self.entries)
        cursor.execute("SELECT * FROM Venue")
        column_names = [desc[0] for desc in cursor.description]
        # Print the column names
        for j, column_name in enumerate(column_names):
            self.entries.append(Entry(self.window, width=40, fg='black'))
            self.entries[j].place(x=(120*(j)), y=80)
            self.entries[j].insert(END, column_name)
        i = 1
        for competition in cursor:
            for j in range(len(competition)):
                self.entries.append(Entry(self.window, width=40, fg='black'))
                self.entries[i*len(competition)+j].place(x=(120*j), y=(25*i)+80)
                self.entries[i*len(competition)+j].insert(END, str(competition[j]))
            i = i+1
    def listJuries(self):
        global cursor
        clearEntries(self.entries)
        cursor.execute("SELECT * FROM JuryInfo")
        column_names = [desc[0] for desc in cursor.description]
        # Print the column names
        for j, column_name in enumerate(column_names):
            self.entries.append(Entry(self.window, width=40, fg='black'))
            self.entries[j].place(x=(120*(j)), y=80)
            self.entries[j].insert(END, column_name)
        i = 1
        for competition in cursor:
            for j in range(len(competition)):
                self.entries.append(Entry(self.window, width=40, fg='black'))
                self.entries[i*len(competition)+j].place(x=(120*j), y=(25*i)+80)
                self.entries[i*len(competition)+j].insert(END, str(competition[j]))
            i = i+1
    def editCompetition(self):
        ent=CompetitionDialog(1)
    def createCompetition(self):
        evnt=CompetitionDialog(0)


class Jury_App:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("1500x600")  # Screen Size(yatay x dikey)
        self.window.resizable(0, 0)
        self.window.config(background="#9BABB8")
        self.window.title("Jury")  # Pencere ismi
        self.entries = []

        button_bg_color = "#2596BE" 
        button_fg_color = "#FFFFFF" 

        list_competition_button = Button(self.window, text="List Competitions",
                                   width=12, height=3, command=self.listCompetitions, bg=button_bg_color, fg=button_fg_color)
        list_competition_button.place(x=2, y=5)
        view_competition_details_button = Button(self.window, text="Attend Competition",
                                           width=12, height=3, command=self.attend_competition, bg=button_bg_color, fg=button_fg_color)
        view_competition_details_button.place(x=142, y=5)
        attend_competition_button = Button(self.window, text="Change Expertise",
                                     width=12, height=3, command=self.changeExpertise, bg=button_bg_color, fg=button_fg_color)
        attend_competition_button.place(x=282, y=5)
        view_organizer_button = Button(self.window, text="List Juries",
                                       width=12, height=3 , command=self.listJurys, bg=button_bg_color, fg=button_fg_color)
        view_organizer_button.place(x=422, y=5)
        add_jury_button = Button(self.window, text="Add Jury",
                                       width=12, height=3, command=self.addJury, bg=button_bg_color, fg=button_fg_color)
        add_jury_button.place(x=562, y=5)

    def listCompetitions(self):
        global cursor
        clearEntries(self.entries)  # Assuming this function clears existing entries

        cursor.execute("""SELECT JuryView.*, Venue.venue_name, Venue.address
                          FROM JuryView
                          LEFT JOIN Venue ON JuryView.venue_id = Venue.venue_id""")
        
        column_names = [desc[0] for desc in cursor.description]

        # Display column names
        column_width = 40  # Adjust width as needed
        for j, column_name in enumerate(column_names):
            entry = Entry(self.window, width=column_width, fg='black')
            entry.place(x=(120 * j), y=80)  # Adjust x position as needed
            entry.insert(END, column_name)
            self.entries.append(entry)

        # Display competition data
        i = 1
        for competition in cursor:
            for j in range(len(competition)):
                entry = Entry(self.window, width=column_width, fg='black')
                entry.place(x=(120 * j), y=(25 * i) + 80)  # Adjust x and y position
                entry.insert(END, str(competition[j]))
                self.entries.append(entry)
            i += 1

    def attend_competition(self):
        ent=CancelCompetitionDialog(1)
    def changeExpertise(self):
        ent = CancelCompetitionDialog(2)
    def addJury(self):
        ent = CancelCompetitionDialog(3)
    def listJurys(self):
        global cursor
        clearEntries(self.entries)
        cursor.execute("SELECT * FROM Jury")
        column_names = [desc[0] for desc in cursor.description]
        # Print the column names
        for j, column_name in enumerate(column_names):
            self.entries.append(Entry(self.window, width=40, fg='black'))
            self.entries[j].place(x=(120*(j)), y=80)
            self.entries[j].insert(END, column_name)
        i = 1
        for competition in cursor:
            for j in range(len(competition)):
                self.entries.append(Entry(self.window, width=40, fg='black'))
                self.entries[i*len(competition)+j].place(x=(120*j), y=(25*i)+80)
                self.entries[i*len(competition)+j].insert(END, str(competition[j]))
            i = i+1


class Competitor_App:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("1500x600")  # Screen Size(yatay x dikey)
        self.window.resizable(0, 0)
        self.window.config(background="#9BABB8")
        self.window.title("Competitor")  # Pencere ismi
        self.entries = []

        button_bg_color = "#2596BE" 
        button_fg_color = "#FFFFFF" 

        list_competition_button = Button(self.window, text="List Competitions",
                                   width=12, height=3, command=self.listCompetitions, bg=button_bg_color, fg=button_fg_color)
        list_competition_button.place(x=2, y=5)
        view_competition_details_button = Button(self.window, text="Buy Ticket",
                                           width=12, height=3, command=self.buyTicket, bg=button_bg_color, fg=button_fg_color)
        view_competition_details_button.place(x=142, y=5)
        list_Ticket_details_button = Button(self.window, text="List All Ticket",
                                           width=12, height=3, command=self.listAllTicket, bg=button_bg_color, fg=button_fg_color)
        list_Ticket_details_button.place(x=282, y=5)
        cancel_ticket_details_button = Button(self.window, text="Cancel Ticket",
                                           width=12, height=3, command=self.cancelTicket, bg=button_bg_color, fg=button_fg_color)
        cancel_ticket_details_button.place(x=422, y=5)
        attend_competition_button = Button(self.window, text="List Competitors",
                                     width=12, height=3, command=self.listCompetitors, bg=button_bg_color, fg=button_fg_color)
        attend_competition_button.place(x=562, y=5)
        view_organizer_button = Button(self.window, text="Add Competitor",
                                       width=12, height=3, command=self.addCompetitor, bg=button_bg_color, fg=button_fg_color)
        view_organizer_button.place(x=702, y=5)

    def listCompetitions(self):
        global cursor
        clearEntries(self.entries)
        cursor.execute("""SELECT CompetitorView.*,Jury.jury_name, Jury.expertise
                  FROM CompetitorView
                  RIGHT JOIN Jury ON CompetitorView.jury_id = Jury.jury_id
                  WHERE CompetitorView.competition_id IS NOT NULL""")
        
        column_names = [desc[0] for desc in cursor.description]
        # Print the column names
        for j, column_name in enumerate(column_names):
            self.entries.append(Entry(self.window, width=40, fg='black'))
            self.entries[j].place(x=(120*(j)), y=80)
            self.entries[j].insert(END, column_name)
        i = 1
        for competition in cursor:
            for j in range(len(competition)):
                self.entries.append(Entry(self.window, width=40, fg='black'))
                self.entries[i*len(competition)+j].place(x=(120*j),y=(25*i)+80)
                self.entries[i*len(competition)+j].insert(END, str(competition[j]))
            i = i+1


    def listCompetitors(self):
        global cursor
        clearEntries(self.entries)
        cursor.execute("SELECT DISTINCT * FROM Competitor")
        column_names = [desc[0] for desc in cursor.description]
        # Print the column names
        for j, column_name in enumerate(column_names):
            self.entries.append(Entry(self.window, width=40, fg='black'))
            self.entries[j].place(x=(120*(j)), y=80)
            self.entries[j].insert(END, column_name)
        i = 1
        for competition in cursor:
            for j in range(len(competition)):
                self.entries.append(Entry(self.window, width=40, fg='black'))
                self.entries[i*len(competition)+j].place(x=(120*j), y=(25*i)+80)
                self.entries[i*len(competition)+j].insert(END, str(competition[j]))
            i = i+1
    def listAllTicket(self):
        global cursor
        clearEntries(self.entries)
        cursor.execute("SELECT * FROM TicketView")
        column_names = [desc[0] for desc in cursor.description]
        # Print the column names
        for j, column_name in enumerate(column_names):
            self.entries.append(Entry(self.window, width=40, fg='black'))
            self.entries[j].place(x=(120*(j)), y=80)
            self.entries[j].insert(END, column_name)
        i = 1
        for competition in cursor:
            for j in range(len(competition)):
                self.entries.append(Entry(self.window, width=40, fg='black'))
                self.entries[i*len(competition)+j].place(x=(120*j), y=(25*i)+80)
                self.entries[i*len(competition)+j].insert(END, str(competition[j]))
            i = i+1
    def addCompetitor(self):
        evnt=CompetitorDialog(0)  
    def buyTicket(self):
        evnt = CompetitorDialog(2)
    def cancelTicket(self):
        evnt = CompetitorDialog(3)


class Visitor_App:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("1500x600")  # Screen Size(yatay x dikey)
        self.window.resizable(0, 0)
        self.window.config(background="#9BABB8")
        self.window.title("Visitor")  # Pencere ismi
        self.entries=[]

        button_bg_color = "#2596BE" 
        button_fg_color = "#FFFFFF" 

        list_competition_button = Button(self.window, text="List Competitions",
                                   width=12, height=3 , command=self.listCompetitions, bg=button_bg_color, fg=button_fg_color)
        list_competition_button.place(x=2, y=5)
        view_competition_details_button = Button(self.window, text="Be Volunteer",
                                           width=12, height=3, command=self.beVolunteer, bg=button_bg_color, fg=button_fg_color)
        view_competition_details_button.place(x=142, y=5)
        list_volunteer_button = Button(self.window, text="List Visitor",
                                  width=12, height=3, command=self.listVisitor, bg=button_bg_color, fg=button_fg_color)
        list_volunteer_button.place(x=282, y=5)
        volunteer_button = Button(self.window, text="Add Visitor",
                                  width=12, height=3, command=self.addVisitor, bg=button_bg_color, fg=button_fg_color)
        volunteer_button.place(x=422, y=5)
        edit_volunteer_button = Button(self.window, text="Edit Visitor",
                                  width=12, height=3, command=self.editVisitor, bg=button_bg_color, fg=button_fg_color)
        edit_volunteer_button.place(x=562, y=5)
        remove_volunteer_button = Button(self.window, text="Remove Visitor",
                                  width=12, height=3, command=self.removeVisitor, bg=button_bg_color, fg=button_fg_color)
        remove_volunteer_button.place(x=702, y=5)

    def listCompetitions(self):
        global cursor
        clearEntries(self.entries)
        cursor.execute("SELECT * FROM VisitorView")

        column_names = [desc[0] for desc in cursor.description]
        # Print the column names
        for j, column_name in enumerate(column_names):
            self.entries.append(Entry(self.window, width=40, fg='black'))
            self.entries[j].place(x=(120*(j)), y=80)
            self.entries[j].insert(END, column_name)
        i = 1
        for competition in cursor:
            for j in range(len(competition)):
                self.entries.append(Entry(self.window, width=40, fg='black'))
                self.entries[i*len(competition)+j].place(x=(120*j), y=(25*i)+80)
                self.entries[i*len(competition)+j].insert(END, str(competition[j]))
            i = i+1

    def listVisitor(self):
        global cursor
        clearEntries(self.entries)
        cursor.execute("SELECT * FROM Visitor")

        column_names = [desc[0] for desc in cursor.description]
        # Print the column names
        for j, column_name in enumerate(column_names):
            self.entries.append(Entry(self.window, width=40, fg='black'))
            self.entries[j].place(x=(120*(j)), y=80)
            self.entries[j].insert(END, column_name)
        i = 1
        for competition in cursor:
            for j in range(len(competition)):
                self.entries.append(Entry(self.window, width=40, fg='black'))
                self.entries[i*len(competition)+j].place(x=(120*j), y=(25*i)+80)
                self.entries[i*len(competition)+j].insert(END, str(competition[j]))
            i = i+1
    def removeVisitor(self):
        env=VisitorDialog(2)
    def addVisitor(self):
        env=VisitorDialog(0)
    def editVisitor(self):
        env=VisitorDialog(1)
    def beVolunteer(self):
        env=VisitorDialog(3)


class CompetitionDialog:
    def __init__(self,type):
        self.root = Tk()
        if type==0:
            self.root.title("Create Competition")
        else:
            self.root.title("Edit Competition")
            competition_id_label = Label(self.root, text="Competition ID:")
            competition_id_label.pack()
            self.competition_id_entry = Entry(self.root)
            self.competition_id_entry.pack()
        
        competition_name_label = Label(self.root, text="Competition Name:")
        competition_name_label.pack()
        self.competition_name_entry = Entry(self.root)
        self.competition_name_entry.pack()

        venue_name_label = Label(self.root, text="Venue ID:")
        venue_name_label.pack()
        self.venue_name_entry = Entry(self.root)
        self.venue_name_entry.pack()

        organizer_name_label = Label(self.root, text="Organizer ID:")
        organizer_name_label.pack()
        self.organizer_name_entry = Entry(self.root)
        self.organizer_name_entry.pack()

        jury_name_label = Label(self.root, text="Jury ID:")
        jury_name_label.pack()
        self.jury_name_entry = Entry(self.root)
        self.jury_name_entry.pack()

        ticket_quantity_label = Label(self.root, text="Ticket Quantity:")
        ticket_quantity_label.pack()
        self.ticket_quantity_entry = Entry(self.root)
        self.ticket_quantity_entry.pack()
        
        visitor_quantity_label = Label(self.root, text="Visitor Quantity:")
        visitor_quantity_label.pack()
        self.visitor_quantity_entry = Entry(self.root)
        self.visitor_quantity_entry.pack()
        if type==1:
            report_id_label = Label(self.root, text="Report ID:")
            report_id_label.pack()
            self.report_id_entry = Entry(self.root)
            self.report_id_entry.pack()

        competition_date_label = Label(self.root, text="Competition Date:")
        competition_date_label.pack()
        self.competition_date_entry = Entry(self.root)
        self.competition_date_entry.pack()

        txt = "Create Competition"
        cmd = self.create_competition
        if type==1:
            txt="Update Competition"
            cmd=self.update_competition
        create_competition_button = Button(
            self.root, text=txt, command=cmd)
        create_competition_button.pack()

    def create_competition(self):
        competition_name = self.competition_name_entry.get()
        venue_id = self.venue_name_entry.get()
        organizer_id = self.organizer_name_entry.get()
        jury_id = self.jury_name_entry.get()
        ticket_quantity = int(self.ticket_quantity_entry.get())
        visitor_quantity = int(self.visitor_quantity_entry.get())
        competition_date = self.competition_date_entry.get()

        global cursor, mydb
        try:
            if not mydb.in_transaction:
                mydb.start_transaction()
            cursor.execute("""INSERT INTO Competition(competition_name,
                       organizer_id,venue_id,ticket_quantity,visitor_quantity,
                       jury_id,report_id,date) values(%s,%s,%s,%s,%s,%s,%s,%s)""",
                       (competition_name,organizer_id,venue_id,ticket_quantity,visitor_quantity,jury_id,None,competition_date))
            cursor.execute("SELECT competition_id FROM Competition ORDER BY competition_id DESC LIMIT 1")
            last_id = cursor.fetchone()[0]
            cursor.execute(
                "UPDATE Jury SET competition_id=%s WHERE jury_id=%s", (last_id, jury_id))
            mydb.commit()
        except mysql.connector.Error as err:
            show_warning(err.msg)
            mydb.rollback()
            
        self.root.destroy()
        
    def update_competition(self):
        competition_id = self.competition_id_entry.get()
        competition_name = self.competition_name_entry.get()
        venue_id = self.venue_name_entry.get()
        organizer_id = self.organizer_name_entry.get()
        jury_id = self.jury_name_entry.get()
        ticket_quantity = int(self.ticket_quantity_entry.get())
        visitor_quantity = int(self.visitor_quantity_entry.get())
        report_id = self.report_id_entry.get()
        competition_date = self.competition_date_entry.get()

        global cursor, mydb
        try:
            cursor.execute("""UPDATE Competition
                            SET competition_name = %s,organizer_id=%s,venue_id=%s,ticket_quantity=%s,
                            visitor_quantity=%s,jury_id=%s,report_id=%s,date = %s
                            WHERE competition_id = %s """,
                           (competition_name, organizer_id, venue_id, ticket_quantity,visitor_quantity, jury_id, report_id, competition_date,competition_id))
        except mysql.connector.Error as err:
            show_warning(err.msg)

        mydb.commit()

        self.root.destroy()
class CancelCompetitionDialog:
    def __init__(self,type):
        self.root = Tk()
        title = "Cancel Competition"
        cmd = self.cancel_competition
        if type==1:
            title="Attend Competition"
            cmd = self.attend_competition
        elif type==2:
            title = "Change Expertise"
            cmd = self.change_expertise
        elif type == 3:
            title = "Add Jury"
            cmd = self.add_jury
            
        self.root.title(title)
        if type == 1 or type ==2:
            jury_id_label = Label(self.root, text="Jury ID:")
            jury_id_label.pack()
            self.jury_id_entry = Entry(self.root)
            self.jury_id_entry.pack()
        if type == 1 or type == 0:
            competition_name_label = Label(self.root, text="Competition ID:")
            competition_name_label.pack()
            self.competition_name_entry = Entry(self.root)
            self.competition_name_entry.pack()
        if type == 3:
            name_label = Label(self.root, text="Name:")
            name_label.pack()
            self.name_entry = Entry(self.root)
            self.name_entry.pack()
        if type == 2 or type==3:
            expertise_label = Label(self.root, text="Expertise:")
            expertise_label.pack()
            self.expertise_entry = Entry(self.root)
            self.expertise_entry.pack()

        create_competition_button = Button(
            self.root, text=title, command=cmd)
        create_competition_button.pack()

    def cancel_competition(self):
        competition_id = self.competition_name_entry.get()

        global cursor, mydb
        try:
            cursor.execute("DELETE FROM Competition WHERE competition_id=%s",
                           (competition_id,))
        except mysql.connector.Error as err:
            show_warning(err.msg)

        mydb.commit()
        self.root.destroy()
    def attend_competition(self):
        competition_id = self.competition_name_entry.get()
        jury_id = self.jury_id_entry.get()

        global cursor, mydb
        try:
            if not mydb.in_transaction:
                mydb.start_transaction()
            cursor.execute("UPDATE Competition SET jury_id= %s WHERE competition_id= %s",
                           (jury_id, competition_id))
            cursor.execute("UPDATE Jury SET competition_id = %s WHERE jury_id = %s",
                           (competition_id,jury_id))
            mydb.commit()
        except mysql.connector.Error as err:
            show_warning(err.msg)
            mydb.rollback()

        self.root.destroy()
    def change_expertise(self):
        expertise = self.expertise_entry.get()
        jury_id = self.jury_id_entry.get()

        global cursor, mydb
        try:
            cursor.execute("UPDATE Jury SET expertise= %s WHERE jury_id= %s",
                           (expertise, jury_id,))
        except mysql.connector.Error as err:
            show_warning(err.msg)

        mydb.commit()
        self.root.destroy()
    def add_jury(self):
        expertise = self.expertise_entry.get()
        name = self.name_entry.get()

        global cursor, mydb
        try:
            cursor.execute("""INSERT INTO Jury(jury_name,competition_id,expertise) values(%s,%s,%s)""",
                           (name,None,expertise))
        except mysql.connector.Error as err:
            show_warning(err.msg)

        mydb.commit()
        self.root.destroy()
class CompetitorDialog:
    def __init__(self, type):
        self.root = Tk()
        title = "Add Competitor"
        cmd = self.create_competitor
        if type == 1:
            title = "Edit Competitor"
            cmd = self.update_competitor
        elif type == 2:
            title = "Buy Ticket"
            cmd = self.buy_ticket
        elif type == 3:
            title = "Cancel Ticket"
            cmd = self.cancel_ticket
            
        self.root.title(title)
        
        if type==1 or type==2 or type==3:
            competitor_id_label = Label(self.root, text="Competitor ID:")
            competitor_id_label.pack()
            self.competitor_id_entry = Entry(self.root)
            self.competitor_id_entry.pack()
        if type==0 or type==1:
            competitor_name_label = Label(self.root, text="Competitor Name:")
            competitor_name_label.pack()
            self.competitor_name_entry = Entry(self.root)
            self.competitor_name_entry.pack()

            age_label = Label(self.root, text="Age:")
            age_label.pack()
            self.age_entry = Entry(self.root)
            self.age_entry.pack()
        if type==2:
            competition_id_label = Label(self.root, text="Competition ID:")
            competition_id_label.pack()
            self.competition_id_entry = Entry(self.root)
            self.competition_id_entry.pack()
        if type == 3:
            ticket_id_label = Label(self.root, text="Ticket ID:")
            ticket_id_label.pack()
            self.ticket_id_entry = Entry(self.root)
            self.ticket_id_entry.pack()
        
        create_competitor_button = Button(
            self.root, text=title, command=cmd)
        create_competitor_button.pack()

    def create_competitor(self):
        competitor_name = self.competitor_name_entry.get()
        age = self.age_entry.get()

        global cursor, mydb
        try:
            cursor.execute("""INSERT INTO Competitor(competitor_name,age,ticket_quantity)values(%s,%s,%s)""",
                           (competitor_name,age,None))
        except mysql.connector.Error as err:
            show_warning(err.msg)

        mydb.commit()
        self.root.destroy()
    def update_competitor(self):
        competitor_id = self.competitor_id_entry.get()
        competitor_name = self.competitor_name_entry.get()
        age = self.age_entry.get()

        global cursor, mydb
        try:
            cursor.execute("UPDATE Competitor SET competitor_name = %s,age=%s WHERE competitor_id = %s",
                           (competitor_name, age, competitor_id))
        except mysql.connector.Error as err:
            show_warning(err.msg)

        mydb.commit()
        self.root.destroy()
    def buy_ticket(self):
        competitor_id = self.competitor_id_entry.get()
        competition_id = self.competition_id_entry.get()

        global cursor, mydb
        try:
            if not mydb.in_transaction:
                mydb.start_transaction()
            cursor.execute("SELECT competition_name, date, venue_id FROM Competition WHERE competition_id= %s",(competition_id,))
            competition_details = cursor.fetchone()
            if competition_details is not None:
                competition_name, competition_date, venue_id = competition_details
                cursor.execute("SELECT venue_name FROM Venue WHERE venue_id= %s", (venue_id,))
                venue_name = cursor.fetchone()
                cursor.execute("""INSERT INTO Ticket(competition_id,competition_name,competition_date,
                                    venue_id,venue_name,competitor_id) values(%s,%s,%s,%s,%s,%s)""",
                            (competition_id,competition_name,competition_date,venue_id,venue_name[0],competitor_id))
                cursor.execute("UPDATE Competition SET ticket_quantity = ticket_quantity -1 WHERE competition_id=%s",
                               (competition_id,))
                cursor.execute("UPDATE Competitor SET ticket_quantity = ticket_quantity +1 WHERE competitor_id=%s",
                               (competitor_id,))
            mydb.commit()
        except mysql.connector.Error as err:
            show_warning(err.msg)
            mydb.rollback()

        self.root.destroy()
    def cancel_ticket(self):
        competitor_id = self.competitor_id_entry.get()
        ticket_id = self.ticket_id_entry.get()

        global cursor, mydb
        try:
            if not mydb.in_transaction:
                mydb.start_transaction()
            cursor.execute("SELECT competition_id FROM Ticket WHERE ticket_id= %s", (ticket_id,))
            competition_id = cursor.fetchone()
            cursor.execute("UPDATE EVENT SET ticket_quantity= ticket_quantity+1 WHERE competition_id= %s",
                           (competition_id[0],))
            cursor.execute("DELETE FROM Ticket WHERE ticket_id= %s AND competitor_id=%s ",
                           (ticket_id,competitor_id))
            cursor.execute("UPDATE Competitor SET ticket_quantity = ticket_quantity -1 WHERE competitor_id=%s",
                           (competitor_id,))
            mydb.commit()   
        except mysql.connector.Error as err:
            mydb.rollback()
            show_warning(err.msg)
            
        self.root.destroy()
class VisitorDialog:
    def __init__(self, type):
        self.root = Tk()
        title = "Add Visitor"
        cmd = self.create_visitor
        if type == 1:
            title = "Edit Visitor"
            cmd = self.update_visitor
        elif type == 2:
            title = "Remove Visitor"
            cmd = self.remove_visitor
        elif type == 3:
            title = "Volunteer"
            cmd = self.be_volunteer

        self.root.title(title)

        if type == 1 or type == 2 or type == 3:
            visitor_id_label = Label(self.root, text="Visitor ID:")
            visitor_id_label.pack()
            self.visitor_id_entry = Entry(self.root)
            self.visitor_id_entry.pack()
        if type == 0 or type == 1:
            visitor_name_label = Label(self.root, text="Visitor Name:")
            visitor_name_label.pack()
            self.visitor_name_entry = Entry(self.root)
            self.visitor_name_entry.pack()

            age_label = Label(self.root, text="Age:")
            age_label.pack()
            self.age_entry = Entry(self.root)
            self.age_entry.pack()
        if type == 3:
            competition_id_label = Label(self.root, text="Competition ID:")
            competition_id_label.pack()
            self.competition_id_entry = Entry(self.root)
            self.competition_id_entry.pack()

        create_competitor_button = Button(
            self.root, text=title, command=cmd)
        create_competitor_button.pack()

    def create_visitor(self):
        visitor_name = self.visitor_name_entry.get()
        age = self.age_entry.get()

        global cursor, mydb
        try:
            cursor.execute("INSERT INTO Visitor(visitor_name,age)values(%s,%s)",(visitor_name, age))
        except mysql.connector.Error as err:
            show_warning(err.msg)

        mydb.commit()
        self.root.destroy()
    def update_visitor(self):
        visitor_id = self.visitor_id_entry.get()
        visitor_name = self.visitor_name_entry.get()
        age = self.age_entry.get()

        global cursor, mydb
        try:
            cursor.execute("UPDATE Visitor SET visitor_name = %s,age=%s WHERE visitor_id = %s",
                           (visitor_name, age, visitor_id))
        except mysql.connector.Error as err:
            show_warning(err.msg)

        mydb.commit()
        self.root.destroy()
    def be_volunteer(self):
        global cursor, mydb
        visitor_id = self.visitor_id_entry.get()
        competition_id = self.competition_id_entry.get()

        try:
            if not mydb.in_transaction:
                mydb.start_transaction()
            cursor.execute("UPDATE Visitor SET competition_id=%s WHERE visitor_id= %s", (competition_id,visitor_id,))
            cursor.execute("UPDATE Competition SET visitor_quantity=visitor_quantity-1 WHERE competition_id= %s", (competition_id,))
            mydb.commit()
        except mysql.connector.Error as err:
            show_warning(err.msg)
            mydb.rollback()

        self.root.destroy()
    def remove_visitor(self):
        visitor_id = self.visitor_id_entry.get()
        global cursor, mydb
        try:
            cursor.execute("DELETE FROM Visitor WHERE visitor_id= %s",(visitor_id,))
        except mysql.connector.Error as err:
            show_warning(err.msg)

        mydb.commit()
        self.root.destroy()

class ReportDialog:
    def __init__(self, type):
        self.root = Tk()
        title = "See Report"
        cmd = self.see_report
        if type == 1:
            title = "Add Report"
            cmd = self.add_report

        self.root.title(title)
        if type == 0:
            report_id_label = Label(self.root, text="Report ID:")
            report_id_label.pack()
            self.report_id_entry = Entry(self.root)
            self.report_id_entry.pack()
        if type == 1:
            competition_id_label = Label(self.root, text="Competition ID:")
            competition_id_label.pack()
            self.competition_id_entry = Entry(self.root)
            self.competition_id_entry.pack()
            
            info_label = Label(self.root, text="Information:")
            info_label.pack()
            self.info_entry = Entry(self.root)
            self.info_entry.pack()

        create_competition_button = Button(
            self.root, text=title, command=cmd)
        create_competition_button.pack()

    def see_report(self):
        report_id = self.report_id_entry.get()
        global cursor, mydb
        try:
            cursor.execute("SELECT details FROM Report WHERE report_id= %s",
                           (report_id ,))
            info=cursor.fetchone()[0]
            messagebox.showinfo("Report",str(info))
        except mysql.connector.Error as err:
            show_warning(err.msg)

        mydb.commit()
        self.root.destroy()

    def add_report(self):
        competition_id = self.competition_id_entry.get()
        info=self.info_entry.get()

        global cursor, mydb
        try:
            cursor.callproc("AddReport", [info])
            cursor.execute(
                "SELECT report_id FROM Report ORDER BY report_id DESC LIMIT 1")
            last_id = cursor.fetchone()[0]
            cursor.execute(
                "UPDATE Competition SET report_id=%s WHERE competition_id=%s", (last_id,competition_id))
        except mysql.connector.Error as err:
            show_warning(err.msg)

        mydb.commit()
        self.root.destroy()


def clearEntries(entries):
    k=len(entries)
    for i in range(k):
        entries.pop().delete(0,END)
        
def show_warning(txt):
    messagebox.showwarning("Warning", txt)

if __name__ == "__main__":
    main_app = Main_App()
    main_app.window.mainloop()
