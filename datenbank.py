import sqlite3
import time
import datetime

def check(uid):
    connection = sqlite3.connect("Arbeiter")
    c = connection.cursor()
    c.execute("SELECT * FROM Arbeiter WHERE UID = ?", (uid))
    result = c.fetchone()
    print(result[0])
    dname = result[0]
    return dname
    
    connection.commit()
    connection.close()

def test(dname):
    connection = sqlite3.connect("Arbeitszeiten")
    c = connection.cursor()

    c.execute("SELECT * FROM "+dname+" WHERE Abfahrtszeit = '00:00:00'")
    result = c.fetchone()
    try:
        if result[3] == "00:00:00":
            update(dname)
    except:
        add(dname)

    connection.commit()
    connection.close()

def add(dname):

    connection = sqlite3.connect("Arbeitszeiten")
    c = connection.cursor()

    tag = datetime.date.today().strftime("%A")
    datum = datetime.date.today()
    ankunftszeit = time.strftime("%H:%M:%S")
    abfahrtszeit = "00:00:00"
    arbeitszeit = "0"
    zeitstempel = time.time()


    c.execute("INSERT INTO "+dname+" (Tag, Datum, Ankunftszeit, Abfahrtszeit, Zeitstempel, Arbeitszeit) VALUES (?, ?, ?, ?, ?, ?)",
          (tag, datum, ankunftszeit, abfahrtszeit, zeitstempel, arbeitszeit))

    connection.commit()
    connection.close()

def update(dname):

    connection = sqlite3.connect("Arbeitszeiten")
    c = connection.cursor()

    abfahrtszeit = time.strftime("%H:%M:%S")

    c.execute("SELECT * FROM "+dname+" WHERE Abfahrtszeit = '00:00:00'")
    zeitstempel = c.fetchone()[4]
    print(zeitstempel)
    zeitjetzt = time.time()
    arbeitszeit = zeitjetzt - zeitstempel
    arbeitszeit = arbeitszeit / 60
    c.execute("UPDATE "+dname+" SET Arbeitszeit = ? WHERE Abfahrtszeit = '00:00:00'",
              ([int(arbeitszeit)]))
    c.execute("UPDATE "+dname+" SET Abfahrtszeit = ? WHERE Abfahrtszeit = '00:00:00'",
              ([abfahrtszeit]))


    connection.commit()
    connection.close()

def read(dname):
    connection = sqlite3.connect("Arbeitszeiten")
    c = connection.cursor()

    c.execute("SELECT * FROM " + dname)
    print(dname + ":")
    result = c.fetchall()
    for r in result:
        print(r)

    connection.commit()
    connection.close()
