from flask import Flask, request, jsonify
from flask_cors import CORS
from webpush import py_webpus

import json

app = Flask(__name__)
CORS(app)

public_key = 'YOUR_PUBLIC_KEY'
private_key = 'YOUR_PRIVATE_KEY'

webpusher = WebPusher(vapid_private_key=private_key, vapid_claims={"sub": "mailto:your@email.com"})
import datetime
from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler(daemon=True)
scheduler.start()

def send_notification(subscription, message):
    try:
        webpusher.send_push_message(subscription, json.dumps(message))
    except Exception as e:
        print('Error sending push notification:', e)

@app.route('/api/set-reminder', methods=['POST'])
def set_reminder():
    data = request.json
    days = int(data['days'])
    times_array = data['timesArray']
    medicine_name = data['medicineName']

    for day in range(1, days + 1):
        for time in times_array:
            notification_time = datetime.datetime.strptime(time, '%H:%M').time()
            scheduled_time = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=day), notification_time)

            # Example: Sending notification after 10 seconds for demonstration
            # In production, use scheduled_time instead
            scheduler.add_job(send_notification, 'date', run_date=datetime.datetime.now() + datetime.timedelta(seconds=10),
                              args=[data['subscription'], {'message': f"It's time to take {medicine_name}!"}])

    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
