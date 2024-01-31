from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Replace 'YOUR_TICKETMASTER_API_KEY' with your actual Ticketmaster API key
TICKETMASTER_API_KEY = os.environ.get('TICKETMASTER_API_KEY')
TICKETMASTER_API_URL = 'https://app.ticketmaster.com/discovery/v2/events.json'

@app.route('/get_events', methods=['GET'])
def get_events():
    # Get the city name from the query parameters
    city = request.args.get('city')

    if not city:
        return jsonify({'error': 'City parameter is missing'}), 400

    # Make a request to the Ticketmaster API
    params = {
        'apikey': TICKETMASTER_API_KEY,
        'city': city,
        'size': 10  # You can adjust the number of events to retrieve
    }

    try:
        response = requests.get(TICKETMASTER_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error connecting to Ticketmaster API: {e}'}), 500

    # Process the API response and extract relevant information
    events = []
    for event in data.get('_embedded', {}).get('events', []):
        event_data = {
            'name': event.get('name'),
            'date': event.get('dates', {}).get('start', {}).get('local'),
            'venue': event.get('_embedded', {}).get('venues', [{}])[0].get('name')
        }
        events.append(event_data)

    return jsonify({'events': events})


if __name__ == '__main__':
    app.run(debug=True)
