import os

from flask import Flask


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'investments.sqlite'),
        INVESTMENT_DATA=os.path.join(app.instance_path, 'investment_data.json')
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import init_db
    init_db.init_app(app)

    return app
