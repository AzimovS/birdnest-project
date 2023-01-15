import json
from threading import Timer
from flask import Flask, jsonify
import sqlite3
import requests
import xmltodict
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MLXH243GssUWwKdTWS7FDhdwYF56wPj8'

URL_DRONE = "https://assignments.reaktor.com/birdnest/drones"
URL_PILOT = "https://assignments.reaktor.com/birdnest/pilots/"
CREATE_SQL = """ CREATE TABLE drones (
                serialNumber text NOT NULL,
                posx text NOT NULL,
                posy text NOT NULL,
                time text NOT NULL,
                distFromCentre text NOT NULL,
                name text NOT NULL,
                email text NOT NULL,
                phoneNumber text not NULL
            ) """
INSERT_SQL = """INSERT INTO drones (serialNumber, posx, posy, time, distFromCentre, name, email, phoneNumber) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
FIND_TIME_SQL = """SELECT MAX(time) FROM drones"""
FIND_VIOLATED_SQL = """SELECT tbl.* FROM drones tbl INNER JOIN
                        (
                        SELECT serialNumber, MIN(distFromCentre) distFromCentre
                        FROM drones
                        GROUP BY serialNumber
                        ) tbl1
                        ON tbl1.serialNumber = tbl.serialNumber
                        WHERE tbl1.distFromCentre = tbl.distFromCentre"""


def db_connection():
    conn = None
    try:
        if os.path.exists('drones.db'):
            conn = sqlite3.connect('drones.db')
        else:
            conn = sqlite3.connect('drones.db')
            conn.execute(CREATE_SQL)
    except:
        print("Something went wrong with db")
    return conn


def get_pilot(serialNumber):
    url = f'{URL_PILOT}{serialNumber}'
    try:
        uResponse = requests.get(url)
    except requests.ConnectionError:
        print("Connection Error")
    Jresponse = uResponse.text
    data = json.loads(Jresponse)
    return f"{data['firstName']} {data['lastName']}", data['email'], data['phoneNumber']


def update_data(interval):
    Timer(interval, update_data, [interval]).start()
    conn = db_connection()
    cur = conn.cursor()
    cx, cy = 250000, 250000
    url = URL_DRONE
    response = requests.get(url)
    try:
        data = xmltodict.parse(response.content)
        for drone in data["report"]['capture']['drone']:
            posX, posY = float(drone['positionX']), float(drone['positionY'])
            timestamp = data["report"]['capture']['@snapshotTimestamp']
            distFromCentre = ((posX - cx) ** 2 + (posY - cy) ** 2) ** 0.5
            if distFromCentre < 100000:
                pilot_name, pilot_email, pilot_phoneNumber = get_pilot(
                    drone['serialNumber'])
                cursor = cur.execute(INSERT_SQL, (drone['serialNumber'], posX, posY,
                                     timestamp, distFromCentre, pilot_name, pilot_email, pilot_phoneNumber))
                conn.commit()
    except:
        print("Failed to parse xml from response")


def clean_data(interval):
    Timer(interval, clean_data, [interval]).start()
    conn = db_connection()
    cur = conn.cursor()
    try:
        # took the max time, because the time on server can be different from the given time.
        recent_date = cur.execute(FIND_TIME_SQL).fetchone()[0]
        time = datetime.datetime.strptime(recent_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        past_time = time - datetime.timedelta(minutes=10)
        delete_sql = f'DELETE FROM drones WHERE time < "{past_time.strftime("%Y-%m-%dT%H:%M:%SZ")}"'
        cur.execute(delete_sql)
        conn.commit()
    except:
        print("Failed to delete entries")


@app.route("/")
def index():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute(FIND_VIOLATED_SQL)
    rows = cur.fetchall()
    drones = []
    for (i, row) in enumerate(rows):
        dct = {}
        dct["serialNumber"] = row[0]
        dct["posX"] = row[1]
        dct["posY"] = row[2]
        dct["time"] = row[3]
        dct['distanceFromCentre'] = row[4]
        dct['name'] = row[5]
        dct['email'] = row[6]
        dct['phoneNumber'] = row[7]
        drones.append(dct)
    response = jsonify(drones)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    # update data every two second
    update_data(2)
    # remove data to avoid overflow
    clean_data(30)
    app.run(debug=False)
