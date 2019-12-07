from flask import request, jsonify, make_response, render_template
from app import app
from app.forms import SearchForm
from data.core import Core
from data.db_adapter import DBAdapter
import datetime
import simplejson as json
from app.carrier import Carrier


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/search', methods=['GET'])
def search():
    date_from = request.args.get('date_from')
    format_str = '%Y-%m-%d'  # The format
    datetime_obj = datetime.datetime.strptime(date_from, format_str)
    departure_date = datetime_obj.strftime('%d.%m.%Y')

    search_util = Core()
    journeys = search_util.getTrains(request.args.get('source'), request.args.get('destination'), departure_date)
    template = render_template('search_results.html', journeys=json.loads(journeys))
    return template


@app.route('/search_form', methods=['GET', 'POST'])
def search_form():
    form = SearchForm(csrf_enabled=False)
    if form.validate_on_submit():
        date_from = request.form.get('departure_date')
        format_str = '%Y-%m-%d'  # The format
        datetime_obj = datetime.datetime.strptime(date_from, format_str)
        departure_date = datetime_obj.strftime('%d.%m.%Y')

        # Using Postgresql
        carrier_util = Carrier()
        journeys = carrier_util.get_journeys(request.form.get('source'), request.form.get('destination'), departure_date)

        db_connector = DBAdapter()
        for journey in journeys:
            db_connector.insert(journey)
        return render_template('search_results.html', journeys=journeys)
    return render_template('search.html', form=form)


@app.route('/create_table')
def create_table():
    db_connector = DBAdapter()
    db_connector.create_table()
    return 'Complete'
