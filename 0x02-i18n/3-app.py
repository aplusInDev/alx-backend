#!/usr/bin/env python3
"""Basic Babel setup"""

from flask import Flask, render_template, request
from flask_babel import Babel
from typing import Union, Dict

app = Flask(__name__)

babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """Config app class"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@app.route('/')
def index() -> str:
    """Index page"""
    return render_template('3-index.html')


@babel.localeselector
def get_locale() -> str:
    """Get locale"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user() -> Union[Dict, None]:
    """Get user"""
    login_id = request.args.get('login_as')
    if login_id:
        return users.get(int(login_id))
    return None


@app.before_request
def before_request() -> None:
    """Before request"""
    user = get_user()
    if user:
        from flask import g
        g.user = user


if __name__ == "__main__":
    app.run()
