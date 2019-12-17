import os
import json

from flask import (Flask, jsonify)


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

    from . import company
    app.register_blueprint(company.bp)

    from . import investor
    app.register_blueprint(investor.bp)

    from . import investment
    app.register_blueprint(investment.bp)

    @app.route('/')
    def hello():
        return jsonify({'success': True}), 200

    return app
