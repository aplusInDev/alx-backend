#!/usr/bin/env python3
"""Basic Babel setup"""

from flask import Flask, render_template, request
from flask_babel import Babel

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
    return render_template('2-index.html')


@babel.localeselector
def get_locale() -> str:
    """Get locale"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


if __name__ == "__main__":
    app.run()
