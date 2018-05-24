import sqlite3
import time
import datetime
import RPi.GPIO as GPIO

def get(uid):
    try:
        connection = sqlite3.connect("Datenbanken/Arbeiter.db")
        c = connection.cursor()
        c.execute("SELECT * FROM Arbeiter WHERE UID = ?", [uid])
        result = c.fetchone()
        dname = str(result[0])
        return dname

        connection.commit()
        connection.close()
    except:
        pass

def check(dname, uid):
    connection = sqlite3.connect("Datenbanken/Arbeitszeiten.db")
    c = connection.cursor()

    c.execute("SELECT * FROM "+dname+" WHERE Abfahrtszeit = '00:00:00'")
    result = c.fetchone()
    try:
        if result[3] == "00:00:00":
            update(dname, uid)
    except:
        add(dname, uid)

    connection.commit()
    connection.close()

def add(dname, uid):

    connection = sqlite3.connect("Datenbanken/Arbeitszeiten.db")
    c = connection.cursor()

    tag = datetime.date.today().strftime("%A")
    datum = datetime.date.today()
    ankunftszeit = time.strftime("%H:%M:%S")
    abfahrtszeit = "00:00:00"
    arbeitszeit = "0"
    zeitstempel = time.time()


    c.execute("INSERT INTO "+dname+" (Tag, Datum, Ankunftszeit, Abfahrtszeit, Zeitstempel, Arbeitszeit) VALUES (?, ?, ?, ?, ?, ?)",
          (tag, datum, ankunftszeit, abfahrtszeit, zeitstempel, arbeitszeit))
    print(dname + "(UID:" + uid + ") kommt")
    connection.commit()
    connection.close()

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(33, GPIO.OUT)
    GPIO.output(33, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(33, GPIO.LOW)

def update(dname, uid):

    connection = sqlite3.connect("Datenbanken/Arbeitszeiten.db")
    c = connection.cursor()

    abfahrtszeit = time.strftime("%H:%M:%S")

    c.execute("SELECT * FROM "+dname+" WHERE Abfahrtszeit = '00:00:00'")
    zeitstempel = c.fetchone()[4]
    zeitjetzt = time.time()
    arbeitszeit = zeitjetzt - zeitstempel
    arbeitszeit = arbeitszeit // 60
    c.execute("UPDATE "+dname+" SET Arbeitszeit = ? WHERE Abfahrtszeit = '00:00:00'",
              ([arbeitszeit]))
    c.execute("UPDATE "+dname+" SET Abfahrtszeit = ? WHERE Abfahrtszeit = '00:00:00'",
              ([abfahrtszeit]))
    print(dname + "(UID:" + uid + ") geht")
    connection.commit()
    connection.close()

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(37, GPIO.OUT)
    GPIO.output(37, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(37, GPIO.LOW)


def read(dname):
    connection = sqlite3.connect("Datenbanken/Arbeitszeiten.db")
    c = connection.cursor()

    c.execute("SELECT * FROM " + dname)
    print(dname + ":")
    result = c.fetchall()
    for r in result:
        print(r)

    connection.commit()
    connection.close()
