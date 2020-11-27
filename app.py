import sqlite3

#Script to create "drug_calculator" database

#Tables are:
#users (id, username, password)
#users_prescriptions_junction (userid, prescriptionid)
#prescriptions (id, frequency)
#prescriptions_drugs_junction (prescriptionid, drugid, quantity)
#drugs (id, name)

#Create DB/Connect to DB
connection = sqlite3.connect("drug_calculator.db")

#Create cursor
cursor = connection.cursor()

def run_statements(statements, cursor, connection):
    for statement in statements:
        cursor.execute(statement)
        connection.commit()

def print_results(cursor):
    field_names = ""
    if len(cursor.description) != 0:
        for field in cursor.description:
            field_names = field_names + field[0] + " | "

    results = cursor.fetchall()

    rows = []

    for result in results:
        row = ""

        for field in result:
            row = row + field + " | "
            
        rows.append(row[:-3])

    print(field_names[:-3])

    for row in rows:
        print(str(row))

user_setup = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL);
"""

prescriptions_setup = """
CREATE TABLE IF NOT EXISTS prescriptions (
    id INTEGER NOT NULL PRIMARY KEY,
    frequency INTEGER NOT NULL);
"""

drugs_setup = """
CREATE TABLE IF NOT EXISTS drugs (
    id INTEGER NOT NULL PRIMARY KEY,
    name VARCHAR(255) NOT NULL);
"""

users_prescriptions_junction_setup = """
CREATE TABLE IF NOT EXISTS 
users_prescriptions_junction (
    userid INTEGER NOT NULL,
    prescriptionid INTEGER NOT NULL,
    FOREIGN KEY(userid) 
        REFERENCES users(id),
    FOREIGN KEY(prescriptionid) 
        REFERENCES prescriptions(id));
"""

prescriptions_drugs_junction_setup = """
CREATE TABLE IF NOT EXISTS 
prescriptions_drugs_junction (
    prescriptionid INTEGER NOT NULL,
    drugid INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    FOREIGN KEY (prescriptionid)
        REFERENCES prescriptions(id),
    FOREIGN KEY (drugid)
        REFERENCES drugs(id));
"""

create_statements = [user_setup, prescriptions_setup,
drugs_setup, users_prescriptions_junction_setup,
prescriptions_drugs_junction_setup]

#Execute table creation statements and commit
run_statements(create_statements, cursor, connection)

insert_users = """
INSERT INTO users(id, username, password)
VALUES(1, "mattg", "secure"),
    (2, "gavm", "verysecure"),
    (3, "steveb", "unhackable");
"""

insert_prescriptions = """
INSERT INTO prescriptions(id, frequency)
VALUES (1, 28),
    (2, 14),
    (3, 7);
"""

insert_drugs = """
INSERT INTO drugs(id, name)
VALUES (1, "Fluoxetine 20mg Tablets"),
    (2, "Caffeine 30mg/100mL solution"),
    (3, "Alcohol 8g/100mL solution");
"""

insert_users_prescription_junction = """
INSERT INTO users_prescriptions_junction
    (userid, prescriptionid)
VALUES (1, 1),
    (2, 2),
    (3, 3);
"""

insert_prescriptions_drugs_junction = """
INSERT INTO prescriptions_drugs_junction
    (prescriptionid, drugid, quantity)
VALUES (1, 1, 28),
    (1, 2, 56),
    (1, 3, 14),
    (2, 2, 28),
    (2, 3, 14),
    (3, 2, 14);
"""

insert_statements = [insert_users, insert_prescriptions,
insert_drugs, insert_users_prescription_junction,
insert_prescriptions_drugs_junction]

run_statements(insert_statements, cursor, connection)

select_statement = """
SELECT users.username, drugs.name FROM users 
    JOIN users_prescriptions_junction ON
    users.id = users_prescriptions_junction.userid
    JOIN prescriptions ON
    users_prescriptions_junction.prescriptionid = 
    prescriptions.id
    JOIN prescriptions_drugs_junction ON
    prescriptions.id = 
    prescriptions_drugs_junction.prescriptionid
    JOIN drugs ON
    prescriptions_drugs_junction.drugid =
    drugs.id;
"""

cursor.execute(select_statement)

print_results(cursor)