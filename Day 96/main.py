import requests
import os
from dotenv import load_dotenv
from flask import Flask, render_template
from datetime import datetime

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("F1_KEY")
API_URL = "https://v1.formula-1.api-sports.io/circuits"

circuits_cache = None
statistics_cache = None
last_update_time = None

def get_headers():
    return {'x-apisports-key': API_KEY}


def safe_get_capacity(capacity):
    if capacity is None:
        return 0
    elif isinstance(capacity, int):
        return capacity
    elif isinstance(capacity, str):
        try:
            return int(capacity.replace(',', ''))
        except (ValueError, AttributeError):
            return 0
    else:
        return 0


def fetch_circuits_from_api():
    try:
        response = requests.get(API_URL, headers=get_headers(), timeout=10)
        response.raise_for_status()
        data = response.json()
        circuits = data.get("response", [])

        if circuits:
            for circuit in circuits:
                capacity = circuit.get('capacity')
                circuit['capacity'] = safe_get_capacity(capacity)
            return circuits
        else:
            return get_test_circuits()

    except requests.exceptions.RequestException as e:
        print(e)
        return get_test_circuits()
    except Exception as e:
        print(e)
        return get_test_circuits()

def get_test_circuits():
    return [{
        'id': 1,
        'name': 'Albert Park Circuit',
        'image': 'https://media.api-sports.io/formula-1/circuits/1.png',
        'competition': {
            'id': 1,
            'name': 'Australia Grand Prix',
            'location': {'country': 'Australia', 'city': 'Melbourne'}
        },
        'first_grand_prix': 1996,
        'laps': 58,
        'length': '5.278 km',
        'race_distance': '306.124 km',
        'lap_record': {
            'time': '1:19.813',
            'driver': 'Charles Leclerc',
            'year': '2024'
        },
        'capacity': 80000,
        'opened': 1953,
        'owner': None
    }]


def calculate_statistics(circuits):
    total_capacity = 0
    countries = set()

    for circuit in circuits:
        total_capacity += circuit.get('capacity', 0)

        country = circuit.get('competition', {}).get('location', {}).get('country')
        if country:
            countries.add(country)

    return {
        'total_circuits': len(circuits),
        'total_capacity': total_capacity,
        'country_count': len(countries)
    }


def update_info():
    global circuits_cache, statistics_cache, last_update_time

    now = datetime.now()

    if (circuits_cache is None or statistics_cache is None or
            last_update_time is None):
        circuits_cache = fetch_circuits_from_api()
        statistics_cache = calculate_statistics(circuits_cache)
        last_update_time = now

@app.route('/')
@app.route('/circuits')
def all_circuits():
    update_info()

    return render_template('circuits.html',
                           circuits=circuits_cache,
                           **statistics_cache)


@app.route('/circuit/<int:circuit_id>')
def circuit_detail(circuit_id):
    update_info()

    circuit = next((c for c in circuits_cache if c.get('id') == circuit_id), None)

    if circuit:
        return render_template('circuit_detail.html', circuit=circuit)
    else:
        return render_template('error.html', message="Circuit not found"), 404


@app.route('/force-refresh')
def force_refresh():
    global circuits_cache, statistics_cache, last_update_time

    circuits_cache = fetch_circuits_from_api()
    statistics_cache = calculate_statistics(circuits_cache)
    last_update_time = datetime.now()

    return {
        'status': 'success',
        'message': f'Data refreshed: {len(circuits_cache)} circuits',
        'timestamp': last_update_time.isoformat()
    }, 200


@app.route('/status')
def status():
    cache_info = {
        'circuits_count': len(circuits_cache) if circuits_cache else 0,
        'last_update': last_update_time.isoformat() if last_update_time else 'Never',
        'cache_age_seconds': (datetime.now() - last_update_time).total_seconds()
        if last_update_time else None,
    }
    return render_template('status.html', **cache_info)


if __name__ == '__main__':
    update_info()
    app.run(debug=True)