from flask import Flask

def create_app():
    app = Flask(__name__)

    DB.init_app(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    myvar = "Twitoff App"

    @app.route("/")
    def root():
        users = User.query.all()
        return render_template('base_html', title='Home', users=users)
    
    @app.route('/bananas')
    def bananas():
        return render_template('base_html', title='Bananas')
    
    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return "database has been reset"
    
    tweet1 = Tweet(id=1, text="ryans 1st tweet", user=ryan)
    DB.session.add(tweet1)

    tweet2 = Tweet(id=2, text="julians 1st tweet", user=julian)
    DB.session.add(tweet2)

    tweet3 = Tweet(id=1, text="ryans 2nd tweet", user=ryan)
    DB.session.add(tweet3)

    tweet4 = Tweet(id=2, text="julians 2nd tweet", user=julian)
    DB.session.add(tweet4)
    
    tweet5 = Tweet(id=1, text="ryans 3rd tweet", user=ryan)
    DB.session.add(tweet5)
    
    tweet6 = Tweet(id=2, text="julians 3rd tweet", user=julian)
    DB.session.add(tweet6)

    app.route('/populate')
    def populate():
        ryan = User(id=1, username='Ryan')
        DB.session.add(ryan)
        julian = User(id=2, username='Julian')
        DB.session.add(julian)

        DB.session.commit()
        return 'the database has been populated'
    
    @app.route('/user', methods=['POST'])
    @app.route('/user/<username>', methods=['GET'])

    def user(username=None, message=''):
        username = username or request.values['user_name']

        if request.method == 'POST':
            add_or_update_user(username)
            message = f'user "{username}" has been sucessfully added!'

        tweets = User.query.filter(User.username==username).one().tweets
        return render_template('user.html', title=username, tweets=tweets, message=message)

    return app
