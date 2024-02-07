#!/usr/bin/env python3
'''Basic app with only single route'''
from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Union, Dict


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


def get_user(user_id: int) -> Union[Dict[str, Union[str, None]], None]:
    """ Get user details based on user ID """
    return users.get(user_id)


@app.before_request
def before_request() -> None:
    '''Before request'''
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale() -> str:
    '''Gets the locale language'''
    url_locale = request.args.get('locale', None)
    if url_locale and url_locale in app.config['LANGUAGES']:
        return url_locale

    user_locale = g.user['locale']
    if user_locale and user_locale in app.config['LANGUAGES']:
        return user_locale

    header_locale = request.headers.get('locale', None)
    if header_locale and header_locale in app.config['LANGUAGES']:
        return header_locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    '''Basic index page'''
    return render_template('6-index.html', user=g.user)


if __name__ == "__main__":
    app.run(port="5000", host="0.0.0.0", debug=True)
