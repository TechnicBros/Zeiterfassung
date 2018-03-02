import sqlite3
connection = sqlite3.connect("Arbeitszeiten")
c = connection.cursor()

sql_command = """
CREATE TABLE Arbeiter1 ( 
Tag, 
Datum DATE, 
Ankunftszeit,
Abfahrtszeit,
Zeitstempel,
Arbeitszeit);"""

c.execute(sql_command)

sql_command = """
CREATE TABLE Arbeiter2 ( 
Tag, 
Datum DATE, 
Ankunftszeit, 
Abfahrtszeit,
Zeitstempel,
Arbeitszeit);"""

c.execute(sql_command)

sql_command = """
    CREATE TABLE Arbeiter3 ( 
    Tag, 
    Datum DATE, 
    Ankunftszeit, 
    Abfahrtszeit,
    Zeitstempel,
    Arbeitszeit);"""

c.execute(sql_command)

connection.commit()
connection.close()
