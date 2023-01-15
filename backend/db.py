import sqlite3

conn = sqlite3.connect('drones.db')

sql_query = """ CREATE TABLE drones (
    serialNumber text NOT NULL,
    posx text NOT NULL,
    posy text NOT NULL,
    time text NOT NULL,
    distFromCentre text NOT NULL,
    name text NOT NULL,
    email text NOT NULL,
    phoneNumber text not NULL
) """

conn.execute(sql_query)
conn.close()