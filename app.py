from flask import Flask, send_file, request
from datetime import datetime
import csv
import os
import requests

app = Flask(__name__)
LOG_FILE = 'logs.csv'

def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}").json()
        return f"{response.get('city', '')}, {response.get('country', '')}"
    except:
        return "Unknown"

@app.route('/pixel.png')
def tracking_pixel():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    location = get_location(ip)

    log_entry = [timestamp, ip, location, user_agent]

    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Timestamp (UTC)', 'IP', 'Location', 'User Agent'])
        writer.writerow(log_entry)

    return send_file('pixel.png', mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
   
