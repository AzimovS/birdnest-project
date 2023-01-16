import json
from threading import Timer
from flask import Flask, jsonify
import requests
import xmltodict
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MLXH243GssUWwKdTWS7FDhdwYF56wPj8'

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


def update_data(interval):
    Timer(interval, update_data, [interval]).start()
    global drones_data, max_time
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
                if drone['serialNumber'] not in drones_data:
                    pilot_name, pilot_email, pilot_phoneNumber = get_pilot(
                        drone['serialNumber'])
                    drones_data[drone['serialNumber']] = {
                        "serialNumber": drone["serialNumber"],
                        "posX": posX, "posY": posY, "time": timestamp, "distFromCentre": distFromCentre,
                        "name": pilot_name, "email": pilot_email, "phoneNumber": pilot_phoneNumber}
                elif drones_data[drone['serialNumber']]['distFromCentre'] > distFromCentre:
                    drones_data[drone['serialNumber']
                                ]['distFromCentre'] = distFromCentre
                    drones_data[drone['serialNumber']]['time'] = timestamp
            max_time = timestamp
    except:
        print("Failed to parse xml from response")


def clean_data(interval):
    Timer(interval, clean_data, [interval]).start()
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


if __name__ == "__main__":
    # update data every two second
    update_data(2)
    # remove data to avoid overflow
    clean_data(3)
    app.run(debug=False)
