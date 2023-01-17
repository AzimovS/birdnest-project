import json
from flask import Flask, jsonify
import requests
import xmltodict
import datetime
from flask_apscheduler import APScheduler
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MLXH243GssUWwKdTWS7FDhdwYF56wPj8'


URL_DRONE = "https://assignments.reaktor.com/birdnest/drones"
URL_PILOT = "https://assignments.reaktor.com/birdnest/pilots/"

drones_data = {}
max_time = ""


def get_pilot(serialNumber):
    url = f'{URL_PILOT}{serialNumber}'
    try:
        uResponse = requests.get(url)
    except requests.ConnectionError:
        print("Connection Error")
    data = json.loads(uResponse.text)
    return f"{data['firstName']} {data['lastName']}", data['email'], data['phoneNumber']


def update_data():
    global drones_data, max_time
    cx, cy = 250000, 250000
    url = URL_DRONE
    response = requests.get(url)
    try:
        data = xmltodict.parse(response.content)
        for drone in data["report"]['capture']['drone']:
            posX, posY = float(drone['positionX']), float(drone['positionY'])
            timestamp = data["report"]['capture']['@snapshotTimestamp']
            distanceFromCentre = ((posX - cx) ** 2 + (posY - cy) ** 2) ** 0.5
            if distanceFromCentre < 100000:
                if drone['serialNumber'] not in drones_data:
                    pilot_name, pilot_email, pilot_phoneNumber = get_pilot(
                        drone['serialNumber'])
                    drones_data[drone['serialNumber']] = {
                        "serialNumber": drone["serialNumber"],
                        "posX": posX, "posY": posY, "time": timestamp, "distanceFromCentre": distanceFromCentre,
                        "name": pilot_name, "email": pilot_email, "phoneNumber": pilot_phoneNumber}
                elif drones_data[drone['serialNumber']]['distanceFromCentre'] > distanceFromCentre:
                    drones_data[drone['serialNumber']
                                ]['distanceFromCentre'] = distanceFromCentre
                    drones_data[drone['serialNumber']]['time'] = timestamp
            max_time = timestamp
    except:
        print("Failed to parse xml from response")


def clean_data():
    global drones_data, max_time
    try:
        # took the max time, because the time on server can be different from the given time.
        time = datetime.datetime.strptime(max_time, "%Y-%m-%dT%H:%M:%S.%fZ")
        past_time = time - datetime.timedelta(minutes=10)
        drones_data = {k: v for k, v in drones_data.items(
        ) if v['time'] > past_time.strftime("%Y-%m-%dT%H:%M:%SZ")}
    except:
        print("Failed to delete entries")


@app.route("/")
def index():
    global drones_data, max_time
    drones = [v for v in drones_data.values()]
    print(drones)
    response = jsonify(drones)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

scheduler = APScheduler()
scheduler.add_job(id = 'Scheduled Task', func=update_data, trigger="interval", seconds=3)
scheduler.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)

# /!\ IMPORTANT /!\ : Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())