from os import getenv
import tweepy

tweet_vect = int
key = getenv("TWITTER_API_KEY")
secret = getenv('TWITTER_API_KEY_SECRET')

TWITTER_AUTH = tweepy.OAuthHandler(key, secret)
TWITTER = tweepy.API(TWITTER_AUTH)

def add_or_update_user(username):
    twitter_user = TWITTER.get_user(screen_name = username)

    db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user).id,
    username == twitter_user

    DB.session.add(db_user)

    tweets = twitter_user.timeline(count=200,
                                   exclude_replieds=True,
                                   include_rts=False,
                                   tweet_mode='extended')
    
    for tweet in tweets:
        db_tweet = Tweet(id=tweet.id, text = tweet.full_text[:300])
        DB.session.add(db_tweet)

    except Exception as e:
    print(f'Error Processing {username}: {e}')
    raise e

    DB.session.commit()