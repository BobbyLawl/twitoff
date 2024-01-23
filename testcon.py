from os import getenv
from openaq import OpenAQ
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from test_aq_dashboard import recorded

api = OpenAQ()
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('my_DB')
DB = SQLAlchemy(app)


class Record(DB.Model):
    '''
    the record function will take information from the database
    to fill a data table. A primary key named id is created strictly
    as an integer value. datetime is created as column restricted to 25
    rows as string objects. the value column will use floats while making
    nullable false will require and entry.
    '''
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f'<Record id={self.id}, datetime={self.datetime}, value={self.value}>'


@app.route('/')
def root():
    '''
    the root function is querying specific data with restrictions
    any value in record that is that hasa value of ten or greater
    should be listed. The return is creating a string with the
    requested information by using a forloop to search through
    all information one by one
    '''
    data = Record.query.filter(Record.value >= 10).all()
    return str([(record.datetime, record.value) for record in data])


def info():
    '''
    The info function gathers measurements from OpenAQ using the
    api to gather them
    '''
    body = api.measurements(city='LA', parameter='pm25')
    dates = []
    for res in body['results']:
        date = res['date']['utc']
        val = res['value']
        dates.append((date, val))

    return dates


@app.shell_context_processor
def make_shell_context():
    '''
    The edit shell function returns an f string that shows
    both the values of the databasze and the record.
    '''
    return {'DB': DB, 'Record': Record}


@app.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    data = info()
    for date, val in data:
        rec = Record(datetime=date, value=val)
        DB.session.add(rec)
    DB.session.commit()

    return 'Data replaced'


def test_aq_dashboard():
    '''
    this should access the test_aq_dashboard.py file
    '''
    get_results_test = recorded(test_aq_dashboard())
    return get_results_test
