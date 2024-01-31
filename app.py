from flask import Flask, request, jsonify, render_template
import requests
import os
#from flask_cors import CORS

app = Flask(__name__, static_url_path='')

#CORS(app)

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


@app.route('/')
def index():
    return render_template('index.html')


TICKETMASTER_IMAGES_API_URL = 'https://app.ticketmaster.com/discovery/v2/events/{}/images.json'

@app.route('/get_event_images_for_event', methods=['GET'])
def get_event_images():
    # Get the event ID from the query parameters
    event_id = request.args.get('id')

    if not event_id:
        return jsonify({'error': 'Event ID parameter is missing, Alex'}), 400

    # Make a request to the Ticketmaster Event Images API
    images_url = TICKETMASTER_IMAGES_API_URL.format(event_id)
    params = {
        'apikey': TICKETMASTER_API_KEY,
        'locale': 'en'  # You can customize the locale if needed
    }

    try:
        response = requests.get(images_url, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error connecting to Ticketmaster Event Images API: {e}'}), 500

    # Extract images from the API response
    #images = data.get('_embedded', {}).get('images', [])
    #data is of type dict
    #print(type(data))
    #keys_list = list(data.keys())
    #print(keys_list)
    #['type', 'id', 'images', '_links']
    images = data.get('images', [])

    return jsonify({'images': images})



if __name__ == '__main__':
    app.run(debug=True)


