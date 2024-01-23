"""OpenAQ Air Quality Dashboard with Flask."""
from os import getenv
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from openaq import OpenAQ

load_dotenv()

API = OpenAQ()


class Config(object):
    '''
    the record class object is setting and retaining
    information about the environment. This will help
    others who access or use this module to have
    the correct settings in place.
    '''


APP = Flask(__name__)
DB = SQLAlchemy(APP)

SECRET_KEY = getenv('SECRET_KEY')
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
ENV = getenv('FLASK_ENV')


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
        return f'< rec self = {self.id}, {self.datetime}, {self.value}>'


def info():
    '''
    The info function gathers measurements from OpenAQ using the
    api to gather it
    '''
    _, body = API.measurements(city='Los Angeles', parameter='pm25')
    date_values = []
    for result in body['results']:
        date = result['date']['utc']
        val = result['value']
        date_values.append((date, val))

    return date_values


@APP.shell_context_processor
def edit_shell():
    '''
    The edit shell function returns an f string that shows
    both the values of the databasze and the record.
    '''
    return {'DB': DB, 'Record': Record}


@APP.route('/')
def root():
    '''
    This is the root module docstring
    '''
    data = Record.query.filter(Record.value >= 10).all()
    return str([(record.datetime, record.value) for record in data])


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    data = info()
    for datetime, value in data:
        record = Record(datetime=datetime, value=value)
        DB.session.add(record)
    DB.session.commit()

    return 'data replaced'
