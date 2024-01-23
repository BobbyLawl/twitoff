from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class User(DB.Model):

    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    username = DB.Column(DB.String, nullable=False)

def __repr__(self):
    return f"User: {self.username}"

class Tweet():

    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey("user.id"), nullable=False)
    user = DB.relationship("User", backref=DB.backref("tweets"), lazy=True)

def __repr__(self):
    return f"User: {self.text}"