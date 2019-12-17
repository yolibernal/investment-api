import sqlite3
import uuid

from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = dict_factory

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def add_company(name, city):
    db = get_db()

    db.execute(
        'INSERT INTO company (name, city) VALUES (?, ?)',
        (name, city)
    )
    db.commit()

    return name


def add_investor(name, city):
    db = get_db()

    db.execute(
        'INSERT INTO investor (name, city) VALUES (?, ?)',
        (name, city)
    )
    db.commit()

    return name


def add_investment(company, investors, investment_stage, round_size, date):
    db = get_db()

    investment_round_id = str(uuid.uuid4())

    # Add investment round
    db.execute(
        'INSERT INTO investment_round (id, company, investment_stage, round_size, date) VALUES (?, ?, ?, ?, ?)',
        (investment_round_id, company, investment_stage, round_size, date)
    )

    # add investments from investment round
    db.executemany(
        'INSERT INTO investment (investment_round_id, investor) VALUES (?, ?)',
        [[investment_round_id, investor] for investor in investors]
    )
    db.commit()


def init_app(app):
    app.teardown_appcontext(close_db)
