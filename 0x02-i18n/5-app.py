#!/usr/bin/env python3
'''Basic app with only single route'''
from flask import Flask, render_template, request, g
from flask_babel import Babel


class Config:
    '''Class for babel configuration'''
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    '''Mocks logged in user'''
    ID = request.args.get('login_as')
    if ID and int(ID) in users:
        return users[int(ID)]
    return None


@app.before_request
def before_request():
    '''Before request'''
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale():
    '''Gets the locale language'''
    default_locale = request.args.get('locale')
    if default_locale:
        return default_locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    '''Basic index page'''
    return render_template('5-index.html', user=g.user)


if __name__ == "__main__":
    app.run(port="5000", host="0.0.0.0", debug=True)
