#!/usr/bin/env python3
"""Basic Babel setup"""

from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Union, Dict
import pytz

app = Flask(__name__)

babel = Babel(app)


class Config:
    """Config app class"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@app.route('/')
def index() -> str:
    """Index page"""
    return render_template('4-index.html')


@babel.localeselector
def get_locale() -> str:
    """Get locale"""
    locale = request.args.get('locale', '')
    if locale in app.config["LANGUAGES"]:
        return locale
    if g.user and g.user['locale'] in app.config["LANGUAGES"]:
        return g.user['locale']
    header_locale = request.headers.get('locale', '')
    if header_locale in app.config["LANGUAGES"]:
        return header_locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


def get_user() -> Union[Dict[str, str], None]:
    """Get user"""
    login_as = request.args.get('login_as')
    if login_as:
        return {
            "name": "Balou",
            "locale": "fr",
            "timezone": "Europe/Paris",
        }
    return None


@app.before_request
def before_request() -> None:
    """Before request"""
    user = get_user()
    if user:
        from flask import g
        g.user = user


@babel.timezoneselector
def get_timezone() -> str:
    """Get timezone"""
    timezone = request.args.get('timezone', '').strip()
    if not timezone and g.user:
        timezone = g.user['timezone']
    try:
        return pytz.timezone(timezone).zone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']


if __name__ == "__main__":
    app.run()
