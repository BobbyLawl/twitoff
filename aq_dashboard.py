"""OpenAQ Air Quality Dashboard with Flask."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openaq


api = openaq.OpenAQ()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(app)


class Record(DB.Model):
    '''
    The record function will take information from the database
    to fill a data table. A primary key named id is created strictly
    as an integer value. datetime is created as column restricted to 25
    rows as string objects. the value column will use floats while making
    nullable false will require and entry.
    '''
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        '''
        The __repr__ function is returning a string that consists
        of the requested values - id, datetime, and value.
        '''
        return f'Record: {self.id}, {self.datetime}, {self.value}'


def get_results():
    '''
    The info function gathers measurements from OpenAQ using the
    api to gather it. We should get two values back, the underscore
    will ignore cause the first value to be ignored
    '''
    _, body = api.measurements(city='Los Angeles', parameter='pm25')
    date_values = []
    for result in body['results']:
        date = result['date']['utc']
        val = result['value']
        date_values.append((date, val))

    return date_values


@app.shell_context_processor
def edit_shell():
    '''
    The edit shell function returns an f string that shows
    both the values of the database and the record.
    '''
    return {'DB': DB, 'Record': Record}


@app.route('/')
def root():

    '''
    The root function is querying the database for records with
    air quality values which are greater than or equal to ten.
    It then constructs a string representation of said records and
    returns a string which will be displayed on a web page when the
    root URL is accessed. 
    '''
    data = Record.query.filter(Record.value >= 10).all()
    return str([f'Record(datetime={record.datetime},\
                value={record.value})' for record in data])


def test_record_model():
    '''
    The test_record_model function checks whether the Record model is 
    working as expected.
    '''
    record = Record(id=1, datetime="2023-10-18T00:00:00Z", value=12.5)
    DB.session.add(record)
    assert repr(record) == "Record: 1, 2023-10-18T00:00:00Z, 12.5"


@app.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    data = (get_results())
    for datetime, value in data:
        record = Record(datetime=datetime, value=value)
        DB.session.add(record)
    DB.session.commit()
    return 'Record data replaced'
