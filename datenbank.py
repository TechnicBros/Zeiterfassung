import sqlite3
import time
import datetime

def add1():

    connection = sqlite3.connect("Arbeitszeiten.db")
    c = connection.cursor()

    tag = datetime.date.today().strftime("%A")
    datum = datetime.date.today()
    ankunftszeit = time.strftime("%H:%M:%S")
    abfahrtszeit = "00:00:00"
    arbeitszeit = "0"
    zeitstempel = time.time()


    c.execute("INSERT INTO Arbeiter1 (Tag, Datum, Ankunftszeit, Abfahrtszeit, Zeitstempel, Arbeitszeit) VALUES (?, ?, ?, ?, ?)",
          (tag, datum, ankunftszeit, abfahrtszeit, zeitstempel, arbeitszeit))

    connection.commit()

    connection.close()

def add2():

    connection = sqlite3.connect("Arbeitszeiten.db")
    c = connection.cursor()

    tag = datetime.date.today().strftime("%A")
    datum = datetime.date.today()
    ankunftszeit = time.strftime("%H:%M:%S")
    abfahrtszeit = "00:00:00"
    arbeitszeit = "0"
    zeitstempel = time.time()


    c.execute("INSERT INTO Arbeiter2 (Tag, Datum, Ankunftszeit, Abfahrtszeit, Zeitstempel, Arbeitszeit) VALUES (?, ?, ?, ?, ?, ?)",
          (tag, datum, ankunftszeit, abfahrtszeit, zeitstempel, arbeitszeit))

    connection.commit()

    connection.close()

def update1():

    connection = sqlite3.connect("Arbeitszeiten.db")
    c = connection.cursor()

    abfahrtszeit = time.strftime("%H:%M:%S")

    c.execute('SELECT * FROM Arbeiter1 WHERE Abfahrtszeit = "00:00:00"')
    zeitstempel = c.fetchone()[4]
    print(zeitstempel)
    zeitjetzt = time.time()
    arbeitszeit = zeitjetzt - zeitstempel
    arbeitszeit = arbeitszeit / 60
    c.execute("UPDATE Arbeiter1 SET Arbeitszeit = ? WHERE Abfahrtszeit = '00:00:00'",
              ([int(arbeitszeit)]))
    c.execute("UPDATE Arbeiter1 SET Abfahrtszeit = ? WHERE Abfahrtszeit = '00:00:00'",
              ([abfahrtszeit]))


    connection.commit()

    connection.close()


def update2():

    connection = sqlite3.connect("Arbeitszeiten.db")
    c = connection.cursor()

    abfahrtszeit = time.strftime("%H:%M:%S")

    c.execute('SELECT * FROM Arbeiter2 WHERE Abfahrtszeit = "00:00:00"')
    zeitstempel = c.fetchone()[4]
    print(zeitstempel)
    zeitjetzt = time.time()
    arbeitszeit = zeitjetzt - zeitstempel
    arbeitszeit = arbeitszeit / 60
    c.execute("UPDATE Arbeiter2 SET Arbeitszeit = ? WHERE Abfahrtszeit = '00:00:00'",
              ([int(arbeitszeit)]))
    c.execute("UPDATE Arbeiter2 SET Abfahrtszeit = ? WHERE Abfahrtszeit = '00:00:00'",
              ([abfahrtszeit]))


    connection.commit()

    connection.close()


def read():
    connection = sqlite3.connect("Arbeitszeiten.db")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Arbeiter1")
    print("Arbeiter1:")
    result = cursor.fetchall()
    for r in result:
        print(r)

    cursor.execute("SELECT * FROM Arbeiter2")
    print("Arbeiter2:")
    result = cursor.fetchall()
    for r in result:
        print(r)

def create():
    connection = sqlite3.connect("Arbeitszeiten.db")

    cursor = connection.cursor()

    sql_command = """
    CREATE TABLE Arbeiter1 ( 
    Tag, 
    Datum DATE, 
    Ankunftszeit,
    Abfahrtszeit,
    Zeitstempel,
    Arbeitszeit);"""

    cursor.execute(sql_command)

    sql_command = """
    CREATE TABLE Arbeiter2 ( 
    Tag, 
    Datum DATE, 
    Ankunftszeit, 
    Abfahrtszeit,
    Zeitstempel,
    Arbeitszeit);"""

    cursor.execute(sql_command)

    connection.commit()
    connection.close()