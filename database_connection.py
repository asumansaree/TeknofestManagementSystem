import mysql.connector

def dropAllDB():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",  # Ensure this is the correct password
    )

    cursor = mydb.cursor()
    cursor.execute("SHOW DATABASES")
    temp = cursor.fetchall()
    dbs = [item[0] for item in temp]
    if "competition_management" in dbs:
        cursor.execute("DROP DATABASE competition_management")
    print("DATABASE DROPPED")


def initialize_connection():

    # dropAllDB()  # Drop the existing database

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
    )

    cursor = mydb.cursor()
    create_database(cursor)
    create_table(cursor,mydb)

    return mydb, cursor

def create_database(cursor):
    cursor.execute("SHOW DATABASES")
    temp = cursor.fetchall()
    databases = [item[0] for item in temp]
    if "competition_management" not in databases:
        cursor.execute("CREATE DATABASE competition_management")

    cursor.execute("USE competition_management")
    print("DATABASE CONNECTED")

def create_table(cursor,conn):
    print("TABLE CONTROL")
    cursor.execute("SHOW TABLES")
    temp = cursor.fetchall()
    tables = [item[0] for item in temp]
    print(tables)

    if "Jury" not in tables:
        cursor.execute("""CREATE TABLE Jury(
            jury_id INT PRIMARY KEY AUTO_INCREMENT,
            jury_name VARCHAR(50),
            competition_id INT NULL,
            expertise VARCHAR(50)
         )""")
        conn.commit()
        addJury(cursor, conn)

    if "Report" not in tables:
        cursor.execute("""CREATE TABLE Report(
            report_id INT PRIMARY KEY AUTO_INCREMENT,
            details VARCHAR(200)
         )""")
        conn.commit()
        createProcedure1(cursor, conn)
        addReport(cursor,conn)
        
    if "Venue" not in tables:
        cursor.execute("""CREATE TABLE Venue(
            venue_id INT PRIMARY KEY AUTO_INCREMENT,
            venue_name VARCHAR(50),
            address VARCHAR(100),
            capacity INT
         )""")
        conn.commit()
        createProcedure2(cursor, conn)
        addVenue(cursor, conn)
        
    if "Organizer" not in tables:
        cursor.execute("""CREATE TABLE Organizer(
            organizer_id INT PRIMARY KEY AUTO_INCREMENT,
            organizer_name VARCHAR(50),
            competition_id INT NULL
         )""")
        conn.commit()
        createProcedure3(cursor, conn)
        addOrganizer(cursor,conn)
        
    if "Visitor" not in tables:
        cursor.execute("""CREATE TABLE Visitor(
            visitor_id INT PRIMARY KEY AUTO_INCREMENT,
            visitor_name VARCHAR(50),
            age INT,
            competition_id INT NULL
         )""")
        conn.commit()
        addVisitor(cursor, conn)

    if "Competitor" not in tables:
        cursor.execute("""CREATE TABLE Competitor(
            competitor_id INT PRIMARY KEY AUTO_INCREMENT,
            competitor_name VARCHAR(50),
            age INT,
            ticket_quantity INT NULL
         )""")
        conn.commit()
        addCompetitor(cursor, conn)
        
    if "Ticket" not in tables:
        cursor.execute("""CREATE TABLE Ticket(
            ticket_id INT PRIMARY KEY AUTO_INCREMENT,
            competition_id INT NULL,
            competition_name VARCHAR(50) NULL,
            competition_date DATE NULL,
            venue_id INT NULL,
            venue_name VARCHAR(50) NULL,
            competitor_id INT NULL
         )""")
        conn.commit()
        addTicket(cursor, conn)
        
    if "Competition" not in tables:
        cursor.execute("""CREATE TABLE Competition(
            competition_id INT PRIMARY KEY AUTO_INCREMENT,
            competition_name VARCHAR(50),
            organizer_id INT NULL,
            venue_id INT NULL,
            ticket_quantity INT,
            visitor_quantity INT,
            jury_id INT NULL,
            report_id INT NULL,
            date DATE 
         )""")
        conn.commit()
        addCompetition(cursor, conn)
        
    print("TABLES CREATED")
    alter_competition_table_query = """
    ALTER TABLE Competition
    ADD CONSTRAINT fk_competition_venue FOREIGN KEY (venue_id) REFERENCES Venue(venue_id),
    ADD CONSTRAINT fk_competition_organizer FOREIGN KEY (organizer_id) REFERENCES Organizer(organizer_id),
    ADD CONSTRAINT fk_competition_jury FOREIGN KEY (jury_id) REFERENCES Jury(jury_id),
    ADD CONSTRAINT fk_competition_report FOREIGN KEY (report_id) REFERENCES Report(report_id)
    """

    alter_organizer_table_query = """
    ALTER TABLE Organizer
    ADD CONSTRAINT fk_organizer_competition FOREIGN KEY (competition_id) REFERENCES Competition(competition_id)
    """

    alter_ticket_table_query = """
    ALTER TABLE Ticket
    ADD CONSTRAINT fk_ticket_competition FOREIGN KEY (competition_id) REFERENCES Competition(competition_id),
    ADD CONSTRAINT fk_ticket_venue FOREIGN KEY (venue_id) REFERENCES Venue(venue_id),
    ADD CONSTRAINT fk_ticket_competitor FOREIGN KEY (competitor_id) REFERENCES Competitor(competitor_id)
    """

    alter_visitor_table_query = """
    ALTER TABLE Visitor
    ADD CONSTRAINT fk_visitor_competition FOREIGN KEY (competition_id) REFERENCES Competition(competition_id)
    """

    alter_jury_table_query = """
    ALTER TABLE Jury
    ADD CONSTRAINT fk_jury_competition FOREIGN KEY (competition_id) REFERENCES Competition(competition_id)
    """
    
    cursor.execute("SHOW CREATE TABLE Competition")
    competition_table_definition = cursor.fetchone()[1]
    if "fk_competition_venue" not in competition_table_definition:
        cursor.execute(alter_competition_table_query)
        addTrigger1(cursor,conn)
        addTrigger2(cursor, conn)
        addTrigger3(cursor, conn)
        addTrigger4(cursor, conn)
        addTrigger6(cursor, conn)

    cursor.execute("SHOW CREATE TABLE Organizer")
    organizer_table_definition = cursor.fetchone()[1]
    if "fk_organizer_competition" not in organizer_table_definition:
        cursor.execute(alter_organizer_table_query)
        
    cursor.execute("SHOW CREATE TABLE Ticket")
    ticket_table_definition = cursor.fetchone()[1]
    if "fk_ticket_competition" not in ticket_table_definition:
        cursor.execute(alter_ticket_table_query)

    cursor.execute("SHOW CREATE TABLE Visitor")
    visitor_table_definition = cursor.fetchone()[1]
    if "fk_visitor_competition" not in visitor_table_definition:
        cursor.execute(alter_visitor_table_query)
        addTrigger5(cursor, conn)
    
    cursor.execute("SHOW CREATE TABLE Jury")
    jury_table_definition = cursor.fetchone()[1]
    if "fk_jury_competition" not in jury_table_definition:
        cursor.execute(alter_jury_table_query)
    
    print("FOREIGN KEYS ADDED")
    
    if "CompetitorView" not in tables:
        createView1(cursor,conn)
    
    if "VisitorView" not in tables:
        createView2(cursor, conn)
    
    if "JuryView" not in tables:
        createView3(cursor, conn)
        
    if"JuryInfo" not in tables:
        createView4(cursor, conn)
        
    if "TicketView" not in tables:
        createView5(cursor, conn)
    print("VIEWS ADDED")
    print("PROCEDURES ADDED")

def addVenue(cursor, conn):
    cursor.callproc("AddVenue",["Room 1","Block A, Floor 1",300])
    cursor.callproc("AddVenue",["Room 2", "Block A, Floor 2", 150])
    cursor.callproc("AddVenue",["Room 3", "Block A, Floor 3", 100])
    cursor.callproc("AddVenue",["Kartal", "Istanbul,Kartal", 200])
    cursor.callproc("AddVenue",["Pendik", "Istanbul,Pendik", 150])
    cursor.callproc("AddVenue",["Kartal 2", "Istanbul,Kartal", 20])
    cursor.callproc("AddVenue",["Room 7", "Block B, Floor 1", 60])
    cursor.callproc("AddVenue",["Room 8", "Block B, Floor 2", 90])
    conn.commit()

def addJury(cursor, conn):
    cursor.execute("INSERT INTO Jury(jury_name,competition_id,expertise) values(%s,%s,%s)",
                   ("Ahmet",2, "History"))
    cursor.execute("INSERT INTO Jury(jury_name,competition_id,expertise) values(%s,%s,%s)",
                   ("Mehmet",1,"Math"))
    cursor.execute("INSERT INTO Jury(jury_name,competition_id,expertise) values(%s,%s,%s)",
                   ("Ayşe", 5, "Science"))
    cursor.execute("INSERT INTO Jury(jury_name,competition_id,expertise) values(%s,%s,%s)",
                   ("Ali", 6, "Human Rights"))
    cursor.execute("INSERT INTO Jury(jury_name,competition_id,expertise) values(%s,%s,%s)",
                   ("Yakup", 7, "Justice"))
    cursor.execute("INSERT INTO Jury(jury_name,competition_id,expertise) values(%s,%s,%s)",
                   ("Talha", 8, "Economy"))
   
    conn.commit()
    
def addReport(cursor, conn):
    cursor.callproc("AddReport", ["PDR report template"])
    cursor.callproc("AddReport", ["first report template"])
    cursor.callproc("AddReport", ["second report template"])
    cursor.callproc("AddReport", ["final report template"])
    cursor.callproc("AddReport", ["demo report template"])
    conn.commit()

def addOrganizer(cursor, conn):
    cursor.callproc("AddOrganizer",["asuman",None])
    cursor.callproc("AddOrganizer",["sare",None])
    cursor.callproc("AddOrganizer",["burcu",None])
    cursor.callproc("AddOrganizer",["ayse",None])
    cursor.callproc("AddOrganizer",["ahmet",None])
    conn.commit()
    
def addCompetitor(cursor, conn):
    cursor.execute("INSERT INTO Competitor(competitor_name,age,ticket_quantity) values(%s,%s,%s)",
                   ("Competitor 1", 18, 0))
    cursor.execute("INSERT INTO Competitor(competitor_name,age,ticket_quantity) values(%s,%s,%s)",
                   ("Competitor 1", 22, 0))
    cursor.execute("INSERT INTO Competitor(competitor_name,age,ticket_quantity) values(%s,%s,%s)",
                   ("Competitor 2", 17, 0))
    cursor.execute("INSERT INTO Competitor(competitor_name,age,ticket_quantity) values(%s,%s,%s)",
                   ("Competitor 3", 16, 0))
    cursor.execute("INSERT INTO Competitor(competitor_name,age,ticket_quantity) values(%s,%s,%s)",
                   ("Competitor 4", 21, 0))
    cursor.execute("INSERT INTO Competitor(competitor_name,age,ticket_quantity) values(%s,%s,%s)",
                   ("Competitor 5", 28, 0))
    cursor.execute("INSERT INTO Competitor(competitor_name,age,ticket_quantity) values(%s,%s,%s)",
                   ("Competitor 6", 34, 0))
    cursor.execute("INSERT INTO Competitor(competitor_name,age,ticket_quantity) values(%s,%s,%s)",
                   ("Competitor 7", 31, 0))
    cursor.execute("INSERT INTO Competitor(competitor_name,age,ticket_quantity) values(%s,%s,%s)",
                   ("Competitor 8", 32, 0))

    conn.commit()

def addVisitor(cursor, conn):
    cursor.execute("INSERT INTO Visitor(visitor_name,age,competition_id) values(%s,%s,%s)",
                   ("Visitor 1",25,None))
    cursor.execute("INSERT INTO Visitor(visitor_name,age,competition_id) values(%s,%s,%s)",
                   ("Visitor 2",20,None))
    cursor.execute("INSERT INTO Visitor(visitor_name,age,competition_id) values(%s,%s,%s)",
                   ("Visitor 3",30,None))
    cursor.execute("INSERT INTO Visitor(visitor_name,age,competition_id) values(%s,%s,%s)",
                   ("Visitor 4",26,None))
    cursor.execute("INSERT INTO Visitor(visitor_name,age,competition_id) values(%s,%s,%s)",
                   ("Visitor 5",19,None))

    conn.commit()

def addCompetition(cursor, conn):
    cursor.execute("INSERT INTO Competition(competition_name,organizer_id,venue_id,ticket_quantity,visitor_quantity,jury_id,report_id,date) values(%s,%s,%s,%s,%s,%s,%s,%s)",
                   ("Competition 1",1,1,150,15, 1,None,"2023-06-26"))
    cursor.execute("INSERT INTO Competition(competition_name,organizer_id,venue_id,ticket_quantity,visitor_quantity,jury_id,report_id,date) values(%s,%s,%s,%s,%s,%s,%s,%s)",
                   ("Competition 2",1,2,100,20, 2,None,"2023-07-22"))
    cursor.execute("INSERT INTO Competition(competition_name,organizer_id,venue_id,ticket_quantity,visitor_quantity,jury_id,report_id,date) values(%s,%s,%s,%s,%s,%s,%s,%s)",
                   ("Competition 3",1,3,60,10, 2,None,"2023-06-15"))
    cursor.execute("INSERT INTO Competition(competition_name,organizer_id,venue_id,ticket_quantity,visitor_quantity,jury_id,report_id,date) values(%s,%s,%s,%s,%s,%s,%s,%s)",
                   ("Competition 4",3,None,300,50, 1,None,"2023-08-26"))
    cursor.execute("INSERT INTO Competition(competition_name,organizer_id,venue_id,ticket_quantity,visitor_quantity,jury_id,report_id,date) values(%s,%s,%s,%s,%s,%s,%s,%s)",
                   ("Competition 5",2,4,20,5, 3,None,"2023-10-21"))
    cursor.execute("INSERT INTO Competition(competition_name,organizer_id,venue_id,ticket_quantity,visitor_quantity,jury_id,report_id,date) values(%s,%s,%s,%s,%s,%s,%s,%s)",
                   ("Competition 6",3,5,50,10, 4,None,"2023-07-12"))
    cursor.execute("INSERT INTO Competition(competition_name,organizer_id,venue_id,ticket_quantity,visitor_quantity,jury_id,report_id,date) values(%s,%s,%s,%s,%s,%s,%s,%s)",
                   ("Competition 7",4,5,40,15, 5,None,"2023-06-5"))
    cursor.execute("INSERT INTO Competition(competition_name,organizer_id,venue_id,ticket_quantity,visitor_quantity,jury_id,report_id,date) values(%s,%s,%s,%s,%s,%s,%s,%s)",
                   ("Competition 8",3,4,30,12, 6,None,"2023-11-09"))

    conn.commit()
    
def addTicket(cursor, conn):
    for i in range(5):
        cursor.execute("INSERT INTO Ticket(competition_id,competition_name,competition_date,venue_id,venue_name,competitor_id) values(%s,%s, %s,%s, %s, %s)",
                       (2, "Competition 2", "2023-07-22",2, "Room 2",1))
    conn.commit()

def dropAllDB():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="DataBase_414",
    )

    cursor = mydb.cursor()
    cursor.execute("SHOW DATABASES")
    temp = cursor.fetchall()
    dbs = [item[0] for item in temp]
    if "competition_management" in dbs:
        cursor.execute("DROP DATABASE competition_management")
    print("DATABASE DROPPED")

def addTrigger1(cursor, conn):
    cursor.execute("""CREATE TRIGGER check_capacity_trigger 
            BEFORE INSERT ON Competition
            FOR EACH ROW
            BEGIN
                DECLARE venue_capacity INT;
    
            SELECT capacity INTO venue_capacity
            FROM Venue
            WHERE venue_id = NEW.venue_id;
            
            IF NEW.ticket_quantity > venue_capacity THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Ticket quantity exceeds venue capacity';
            END IF;
            END;""")
    conn.commit()

def addTrigger2(cursor, conn):
    cursor.execute("""CREATE TRIGGER check_future_date_trigger
                BEFORE INSERT ON Competition
                FOR EACH ROW
                BEGIN
                    IF NEW.date <= CURDATE() THEN
                        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Competition date must be in the future';
                    END IF;
                END;""")
    conn.commit()

def addTrigger3(cursor, conn):
    cursor.execute("""CREATE TRIGGER check_month_until_competition_delete_trigger
                BEFORE DELETE ON Competition
                FOR EACH ROW
                BEGIN
                    IF OLD.date <= DATE_ADD(CURDATE(), INTERVAL 1 MONTH) THEN
                        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Competition must be at least one month away';
                    END IF;
                END;""")
    conn.commit()

def addTrigger4(cursor, conn):
    cursor.execute("""CREATE TRIGGER check_ticket_quantity_trigger
                BEFORE UPDATE ON Competition
                FOR EACH ROW
                BEGIN
                    IF NEW.ticket_quantity < 0 THEN
                        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No Ticket';
                    END IF;
                END;""")
    conn.commit()

def addTrigger5(cursor, conn):
    cursor.execute("""CREATE TRIGGER check_visitor_age_trigger
                BEFORE UPDATE ON Visitor
                FOR EACH ROW
                BEGIN
                    IF OLD.age < 18 THEN
                        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Visitor age must be at least 18.';
                    END IF;
                END;""")
    conn.commit()

def addTrigger6(cursor, conn):
    cursor.execute("""CREATE TRIGGER check_visitor_quantity_trigger
                BEFORE UPDATE ON Competition
                FOR EACH ROW
                BEGIN
                    IF NEW.visitor_quantity < 0 THEN
                        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No Need For Visitor';
                    END IF;
                END;""")
    conn.commit()

# Competitors can’t see report_id and visitor_quantity.
def createView1(cursor, conn):
    cursor.execute("""CREATE VIEW CompetitorView AS
                SELECT competition_id,competition_name,organizer_id,venue_id,ticket_quantity,jury_id,date
                FROM Competition;""")
    conn.commit()

# Visitor can’t see report_id.
def createView2(cursor, conn):
    cursor.execute("""CREATE VIEW VisitorView AS
                SELECT competition_name,organizer_id,venue_id,ticket_quantity,visitor_quantity,jury_id,date
                FROM Competition;""")
    conn.commit()

# Juries can’t see competitions that have juries.
def createView3(cursor, conn):
    cursor.execute("""CREATE VIEW JuryView AS
                SELECT competition_id,competition_name,organizer_id,venue_id,jury_id,date
                FROM Competition 
                WHERE jury_id IS NULL;""")
    conn.commit()

# Juries can see other juries competitions
def createView4(cursor, conn):
    cursor.execute("""CREATE VIEW JuryInfo AS
            SELECT Jury.*,Competition.competition_name,Competition.date
            FROM Jury,Competition
            WHERE Jury.competition_id = Competition.competition_id;""")
    conn.commit()

# Competitors can see juries name and expertise
def createView5(cursor, conn):
    cursor.execute("""CREATE VIEW TicketView AS
            SELECT Ticket.*,Jury.jury_name,Jury.expertise
            FROM Ticket,Jury
            WHERE Jury.competition_id = Ticket.competition_id;""")
    conn.commit()

def createProcedure1(cursor,conn):
    cursor.execute("""CREATE PROCEDURE AddReport(IN Info VARCHAR(200))
                    BEGIN
                        INSERT INTO Report(details) values(Info);
                    END;""")
    conn.commit()

def createProcedure2(cursor, conn):
    cursor.execute("""CREATE PROCEDURE AddVenue(IN name VARCHAR(50),IN addr VARCHAR(100),IN cap INT)
                    BEGIN
                        INSERT INTO Venue(venue_name,address,capacity) values(name,addr,cap);
                    END;""")
    conn.commit()

def createProcedure3(cursor,conn):
    cursor.execute("""CREATE PROCEDURE AddOrganizer(IN name VARCHAR(50),IN id INT)
                    BEGIN
                        INSERT INTO Organizer(organizer_name,competition_id) values(name,id);
                    END;""")
    conn.commit()
