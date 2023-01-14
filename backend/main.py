from threading import Timer
from flask import Flask
import sqlite3
import urllib3
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

def update_data(interval):
    conn = db_connection()
    cur = conn.cursor()
    Timer(interval, update_data, [interval]).start()
    url = 'https://assignments.reaktor.com/birdnest/drones'
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    try:
        data = xmltodict.parse(response.data)
        sql = """INSERT INTO drones (serialNumber, posx, posy, time) VALUES (?, ?, ?, ?)"""
        for drone in data["report"]['capture']['drone']:
            cursor = cur.execute(sql, (drone['serialNumber'], drone['positionX'], drone['positionY'], data["report"]['capture']['@snapshotTimestamp']))
            conn.commit()
    except:
        print("Failed to parse xml from response (%s)")
    return data


def clean_data(interval):
    conn = db_connection()
    cur = conn.cursor()
    Timer(interval, clean_data, [interval]).start()
    try:
        # took the max time, because the time on server can be different from the given time.
        sql = f'SELECT MAX(time) FROM drones'
        print(sql)
        recent_date = cur.execute(sql).fetchone()[0]
        date = recent_date.split('T')[0]
        hour = recent_date.split('T')[1].split(':')[0]
        minute = recent_date.split('T')[1].split(':')[1]
        print(minute)
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
clean_data(59)


@app.route("/")
def index():
    return "HI"

if __name__ == "__main__":
    app.run(debug=False)