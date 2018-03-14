import sqlite3
import time
import datetime
import RPi.GPIO as GPIO

def get(uid):
    try:
        connection = sqlite3.connect("Arbeiter")
        c = connection.cursor()
        c.execute("SELECT * FROM Arbeiter WHERE UID = ?", [uid])
        result = c.fetchone()
        dname = result[0]
        return dname

        connection.commit()
        connection.close()
    except:
        print("Die UID konnte nicht zugeordnet werden!")
        pass

def check(dname):
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
    print(dname + " kommt")
    connection.commit()
    connection.close()

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(33, GPIO.OUT)
    GPIO.output(33, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(33, GPIO.LOW)

def update(dname):

    connection = sqlite3.connect("Arbeitszeiten")
    c = connection.cursor()

    abfahrtszeit = time.strftime("%H:%M:%S")

    c.execute("SELECT * FROM "+dname+" WHERE Abfahrtszeit = '00:00:00'")
    zeitstempel = c.fetchone()[4]
    zeitjetzt = time.time()
    arbeitszeit = zeitjetzt - zeitstempel
    arbeitszeit = arbeitszeit / 60
    c.execute("UPDATE "+dname+" SET Arbeitszeit = ? WHERE Abfahrtszeit = '00:00:00'",
              ([int(arbeitszeit)]))
    c.execute("UPDATE "+dname+" SET Abfahrtszeit = ? WHERE Abfahrtszeit = '00:00:00'",
              ([abfahrtszeit]))
    print(dname + " geht")
    connection.commit()
    connection.close()

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(37, GPIO.OUT)
    GPIO.output(37, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(37, GPIO.LOW)


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
