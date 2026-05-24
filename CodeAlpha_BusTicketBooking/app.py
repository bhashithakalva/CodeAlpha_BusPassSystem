from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore
import random

app = Flask(__name__)

# Firebase setup
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route('/')
def home():
    return render_template('index.html', error=None)


@app.route('/book', methods=['POST'])
def book():

    name = request.form['name']
    source = request.form['source']
    destination = request.form['destination']
    date = request.form['date']
    bus_type = request.form['bus_type']
    if source == destination:

        return render_template(
            'success.html',
            error="Source and Destination cannot be same!"
        )
    seats = int(request.form['seats'])

    # Automatic pricing
    distances = {

    ("Hyderabad", "Vijayawada"): 275,
    ("Hyderabad", "Visakhapatnam"): 620,
    ("Hyderabad", "Tirupati"): 560,
    ("Vijayawada", "Visakhapatnam"): 350,
    ("Vijayawada", "Tirupati"): 380,
    ("Guntur", "Nellore"): 290,
    ("Kurnool", "Hyderabad"): 220,
    ("Rajahmundry", "Visakhapatnam"): 190

}

    distance = distances.get((source, destination))

    if distance is None:
        distance = distances.get((destination, source), 250)

    price_per_seat = distance * 2
    price = price_per_seat * seats

    if bus_type == "Super Luxury":
        price += 200

    elif bus_type == "Sleeper":
        price += 400

    elif bus_type == "AC Sleeper":
        price += 700

    # Unique ticket ID
    ticket_id = random.randint(10000, 99999)

    # Store data in Firebase cloud database
    ticket_data = {
        "name": name,
        "source": source,
        "destination": destination,
        "seats": seats,
        "price": price,
        "ticket_id": ticket_id,
        "date": date,
        "bus_type": bus_type,
        "distance": distance,
    }

    db.collection('tickets').add(ticket_data)

    return render_template(
        'success.html',
        name=name,
        source=source,
        destination=destination,
        seats=seats,
        price=price,
        ticket_id=ticket_id,
        date=date,
        bus_type=bus_type,
        distance=distance
    )


if __name__ == '__main__':
    app.run(debug=True)