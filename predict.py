from sklearn.linear_model import LogisticRegression
import numpy as np
from .models import User
from .twitter import tweet_vect

def predict_user(User0_username, user1_username, hypo_tweet_text):

    user0 = User.query.filter(User.username==user0_username).one()
    user1 = User.query.filter(User.username==user1_username).one()

    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    X_train = np.vstack([user0_vects, user1_vects])

    zeros = np.zeros(user0_vects.shape[0])
    ones = np.zeros(user1_vects.shape[0])

    y_train = np.concatenate([zeros, ones])

    hypo_tweet_vect = tweet_vect(hypo_tweet_text).reshape(1, -1)

    return log_rep.predict(hypo_tweet_vect)[0]


------


    @app.shell_context_processor
def edit_shell():
    '''
    The edit shell function returns an f string that shows
    both the values of the databasze and the record.
    '''
    return f'(shell edit = {Record}, {DB})'


def info():
    '''
    The info function gathers measurements from OpenAQ using the
    api to gather it
    '''
    body = api.measurements(city='LA', parameter='pm25')
    dates = []
    for res in body['my results']:
        date = res['date time object']['UC time']
        val = res['my valuw']
        dates.append((date, val))

    return dates


@app.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    data = info()
    for date, val in data:
        rec = Record(date=date, val=val)
        DB.session.add(rec)
    DB.session.commit()

    return 'data replaced'