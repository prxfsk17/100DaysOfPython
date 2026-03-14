import dateutil
from flask import Flask, render_template, url_for, request, session
from datetime import datetime
from werkzeug.utils import redirect
from fetch_data import fetch_teams_from_api, fetch_drivers_from_api, fetch_circuits_from_api

app = Flask(__name__)

circuits_cache = None
teams_cache = None
drivers_cache = []
statistics_circuits_cache = None
last_update_time = None

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

def update_circuits_info():
    global circuits_cache, statistics_circuits_cache, last_update_time
    if circuits_cache is None or statistics_circuits_cache is None or last_update_time is None:
        circuits_cache = fetch_circuits_from_api()
        statistics_circuits_cache = calculate_statistics(circuits_cache)
        last_update_time = datetime.now()


def update_teams_info():
    global teams_cache, last_update_time
    if teams_cache is None or last_update_time is None:
        teams_cache = fetch_teams_from_api()
        last_update_time = datetime.now()


def update_drivers_info():
    global drivers_cache, last_update_time
    if drivers_cache is None or last_update_time is None:
        drivers_cache = []
        last_update_time = datetime.now()


@app.context_processor
def utility_processor():
    def format_number(value):
        try:
            return "{:,}".format(value)
        except:
            return value

    def cache_age_minutes():
        if last_update_time:
            delta = datetime.now() - last_update_time
            return round(delta.total_seconds() / 60, 1)
        return None

    def get_cache_status():
        if last_update_time is None:
            return 'error'
        delta = datetime.now() - last_update_time
        if delta.total_seconds() < 300:  # 5 минут
            return 'fresh'
        else:
            return 'stale'

    return {
        'now': datetime.now(),
        'current_year': datetime.now().year,
        'app_name': 'F1 Circuits',
        'format_number': format_number,
        'cache_age': cache_age_minutes(),
        'cache_status': get_cache_status(),
        'last_update': last_update_time
    }


@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    if isinstance(date, str):
        date = dateutil.parser.parse(date)
    native = date.replace(tzinfo=None)
    format = '%b %d, %Y - %H:%M'
    return native.strftime(format)

@app.template_filter('safe_int')
def safe_int_filter(value):
    try:
        return int(value) if value is not None else 0
    except:
        return 0

@app.template_filter('to_datetime')
def to_datetime_filter(date_string):
    if isinstance(date_string, str):
        try:
            from datetime import datetime
            return datetime.strptime(date_string, '%Y-%m-%d')
        except:
            return None
    return date_string

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/teams')
def all_teams():
    update_teams_info()
    return render_template('teams.html', teams=teams_cache)

@app.route('/driver_search')
def drivers_search():
    return render_template('driver_search.html')

@app.route('/drivers')
def all_drivers():
    return render_template('drivers.html', drivers=drivers_cache)

@app.route('/circuits')
def all_circuits():
    update_circuits_info()
    return render_template('circuits.html',
                           circuits=circuits_cache,
                           **statistics_circuits_cache)

@app.route('/circuit/<int:circuit_id>')
def circuit_detail(circuit_id):
    update_circuits_info()
    circuit = next((c for c in circuits_cache if c.get('id') == circuit_id), None)

    if circuit:
        return render_template('circuit_detail.html', circuit=circuit)
    else:
        return render_template('error.html', message="Circuit not found"), 404

@app.route('/team/<int:team_id>')
def team_detail(team_id):
    update_teams_info()
    team = next((t for t in teams_cache if t.get('id') == team_id), None)
    if team:
        return render_template('team_detail.html', team=team)
    else:
        return render_template('error.html', message="Team not found"), 404

@app.route('/driver/<int:driver_id>')
def driver_detail(driver_id):
    update_drivers_info()
    driver = next((d for d in drivers_cache if d.get('id') == driver_id), None)

    if driver:
        return render_template('driver_detail.html', driver=driver)
    else:
        return render_template('error.html', message="Driver not found"), 404

@app.route('/driver/search')
def search_driver():
    global drivers_cache

    search_query = request.args.get('search', '').strip()

    if len(search_query) < 3:
        return render_template('drivers.html',
                               error="Search query must be at least 3 characters long",
                               search_query=search_query)
    drivers = fetch_drivers_from_api(search_query)
    if not drivers:
        return render_template('drivers.html',
                               error=f"No drivers found matching '{search_query}'",
                               search_query=search_query)
    if len(drivers)==1:
        return render_template('driver_detail.html', driver=drivers[0])
    else:
        drivers_cache = drivers
        return redirect(url_for('all_drivers'))

@app.route('/force-refresh')
def force_refresh():
    global circuits_cache, teams_cache, drivers_cache, statistics_circuits_cache, last_update_time

    circuits_cache = fetch_circuits_from_api()
    teams_cache = fetch_teams_from_api()
    drivers_cache = []
    statistics_circuits_cache = calculate_statistics(circuits_cache)
    last_update_time = datetime.now()

    # return {
    #     'status': 'success',
    #     'message': f'Data refreshed: {len(circuits_cache)} circuits',
    #     'timestamp': last_update_time.isoformat()
    # }, 200
    return redirect(url_for('home'))


@app.route('/status')
def status():
    cache_info = {
        'circuits_count': len(circuits_cache) if circuits_cache else 0,
        'last_update': last_update_time if last_update_time else 'Never',
        'cache_age_seconds': (datetime.now() - last_update_time).total_seconds()
        if last_update_time else None,
    }
    return render_template('status.html', **cache_info)

if __name__ == '__main__':
    update_circuits_info()
    app.run(debug=True)
