import sqlite3
import datetime
#import xlsxwriter


def addDay(dname):
    # Variablen
    datum = datetime.date.today()
    tag = datetime.date.today().strftime("%A")
    pausenzeit = 0
    all = 0

    # Ankuftszeit
    connection = sqlite3.connect("/home/pi/Zeiterfassung/Datenbanken/Arbeitszeiten.db")
    c = connection.cursor()
    c.execute("SELECT * FROM " + dname + " WHERE Datum = ?", [datum])
    result1 = c.fetchone()
    ankunftszeit = result1[2]
    print("Ankunftszeit: " + ankunftszeit)

    # Abfahrtszeit
    c.execute("SELECT * FROM " + dname + " WHERE Datum = ?", [datum])
    result = c.fetchall()
    items = len(result)
    items = items - 1
    items = int(items)
    test = result[items]
    abfahrtszeit = test[3]
    print("Abfahrtszeit: " + abfahrtszeit)

    # Arbeitszeit
    c.execute("SELECT * FROM " + dname + " WHERE Datum = ?", [datum])
    result = c.fetchall()
    for r in result:
        all = all + int(r[5])
    print("Arbeitszeit: " + str(all))
    arbeitszeit = all

    connection.commit()
    connection.close()

    # Datenbank beschreiben
    connection = sqlite3.connect("/home/pi/Zeiterfassung/Datenbanken/Arbeitszeiten-taeglich.db")
    c = connection.cursor()

    c.execute(
        "INSERT INTO " + dname + " (Tag, Datum, Ankunftszeit, Abfahrtszeit, Arbeitszeit, Pausenzeit) VALUES (?, ?, ?, ?, ?, ?)",
        (tag, datum, ankunftszeit, abfahrtszeit, arbeitszeit, pausenzeit))
    connection.commit()
    connection.close()

def addMonth(dname):
    Arbeitszeit = 0
    datum = datetime.date.today()
    datum = str(datum)
    mon = datum[5:7]
    mon = int(mon) - 1
    if len(str(mon)) == 1:
        mon = "0" + str(mon)
    monat = datum[0:5] + mon
    monat1 = "%" + monat + "%"
    print(monat)

    connection = sqlite3.connect("/home/pi/Zeiterfassung/Datenbanken/Arbeitszeiten-taeglich.db")
    c = connection.cursor()

    c.execute("SELECT * FROM " + dname + " WHERE Datum Like ?", [monat1])
    result = c.fetchall()
    for r in result:
        print(r)
        Arbeitszeit = Arbeitszeit + r[4]

    connection.commit()
    connection.close()

    print("Arbeitszeit: " + Arbeitszeit)
    connection = sqlite3.connect("/home/pi/Zeiterfassung/Datenbanken/Arbeitszeiten-monatlich.db")
    c = connection.cursor()
    c.execute("INSERT INTO " + dname + " (Monat, Arbeitszeit) VALUES (?, ?)", (monat, Arbeitszeit))

def closeDay(dname):
    abfahrtszeit = "x"

    connection = sqlite3.connect("/home/pi/Zeiterfassung/Datenbanken/Arbeitszeiten.db")
    c = connection.cursor()

    c.execute("SELECT * FROM " + dname + " WHERE Abfahrtszeit = '00:00:00'")
    result = c.fetchone()
    if result != None:
        datum = datetime.date.today()
        print(str(datum) + ": " + dname + " hat sich nicht abgemeldet!")
        log = open("log.txt", "a")
        log.write("\n" + str(datum) + ": " + dname + " hat sich nicht abgemeldet!")
        log.close()

    c.execute("UPDATE " + dname + " SET Abfahrtszeit = ? WHERE Abfahrtszeit = '00:00:00'",
              ([abfahrtszeit]))

    connection.commit()
    connection.close()

# Nicht fertig
def exportExel():
    # Variablen
    row = 0
    col = 0

    # Worksheet erstellen
    workbook = xlsxwriter.Workbook('Expenses01.xlsx')
    worksheet = workbook.add_worksheet()

    # Datenbank auslesen
    connection = sqlite3.connect("Arbeitszeiten")
    c = connection.cursor()

    c.execute("SELECT * FROM " + dname)
    print("Arbeiter1" + ":")
    result = c.fetchall()
    for r in result:
        print(r)
    connection.commit()
    connection.close()

    # In Excel schreiben
    for tag, datum, ankunftszeit, abfahrtszeit, zeitstempel, arbeitszeit in (result):
        # Convert the date string into a datetime object.
        abfahrtszeit = str(abfahrtszeit)
        arbeitszeit = int(arbeitszeit)
        worksheet.write_string(row, col, tag)
        worksheet.write_string(row, col + 1, datum)
        worksheet.write_string(row, col + 2, ankunftszeit)
        worksheet.write_string(row, col + 3, abfahrtszeit)
        worksheet.write_number(row, col + 4, arbeitszeit)
        row += 1

    workbook.close()