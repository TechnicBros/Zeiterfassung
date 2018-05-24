import sqlite3
import cron

connection = sqlite3.connect("/home/pi/Zeiterfassung/Datenbanken/Arbeiter.db")
c = connection.cursor()
c.execute("SELECT * FROM Arbeiter")
result = c.fetchall()
for r in result:
    dname = r[0]
    print(dname)
    cron.closeDay(dname)
    cron.addDay(dname)