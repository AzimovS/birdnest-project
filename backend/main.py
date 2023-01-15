import json
from threading import Timer
from flask import Flask, jsonify
import sqlite3
import urllib3
import requests
import xmltodict

app = Flask(__name__)


app.config['SECRET_KEY'] = 'MLXH243GssUWwKdTWS7FDhdwYF56wPj8'  # TO DO hide it

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect('drones.db')
    except:
        print("Something went wrong with db")
    return conn

def get_pilot(serialNumber): 
    url = f'https://assignments.reaktor.com/birdnest/pilots/{serialNumber}'
    try:
        uResponse = requests.get(url)
    except requests.ConnectionError:
       return "Connection Error"  
    Jresponse = uResponse.text
    data = json.loads(Jresponse)
    return f"{data['firstName']} {data['lastName']}", data['email'], data['phoneNumber']

def update_data(interval):
    conn = db_connection()
    cur = conn.cursor()
    cx, cy = 250000, 250000
    Timer(interval, update_data, [interval]).start()
    url = 'https://assignments.reaktor.com/birdnest/drones'
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    try:
        data = xmltodict.parse(response.data)
        sql = """INSERT INTO drones (serialNumber, posx, posy, time, distFromCentre, name, email, phoneNumber) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        for drone in data["report"]['capture']['drone']:
            posX, posY = float(drone['positionX']), float(drone['positionY'])
            timestamp = data["report"]['capture']['@snapshotTimestamp']
            distFromCentre = ((posX - cx) ** 2 + (posY - cy) ** 2) ** 0.5
            if distFromCentre < 100000:
                pilot_name, pilot_email, pilot_phoneNumber = get_pilot(drone['serialNumber'])
                cursor = cur.execute(sql, (drone['serialNumber'], posX, posY, timestamp, distFromCentre, pilot_name, pilot_email, pilot_phoneNumber))
                conn.commit()
    except:
        print("Failed to parse xml from response")
    return data


def clean_data(interval):
    conn = db_connection()
    cur = conn.cursor()
    Timer(interval, clean_data, [interval]).start()
    try:
        # took the max time, because the time on server can be different from the given time.
        sql = f'SELECT MAX(time) FROM drones'
        recent_date = cur.execute(sql).fetchone()[0]
        date = recent_date.split('T')[0]
        hour = recent_date.split('T')[1].split(':')[0]
        minute = recent_date.split('T')[1].split(':')[1]
        if minute > '11':
            minute = str(int(minute) - 10)
            old_date = f"{date}T{hour}:{minute}"
            print(old_date)
            sql = f'DELETE FROM drones WHERE time < "{old_date}"'
            cur.execute(sql)
        conn.commit()
    except:
        print("Failed to delete entries (%s)")
    return ""

# update data every two second
update_data(2)

# remove data to avoid overflow
clean_data(60)
    

@app.route("/")
def index():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("""SELECT tbl.* FROM drones tbl INNER JOIN
    (
    SELECT serialNumber, MIN(distFromCentre) distFromCentre
    FROM drones
    GROUP BY serialNumber
    ) tbl1
    ON tbl1.serialNumber = tbl.serialNumber
    WHERE tbl1.distFromCentre = tbl.distFromCentre""")
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
    app.run(debug=False)