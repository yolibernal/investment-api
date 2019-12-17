import sqlite3

import click

from flask import current_app, g
from flask.cli import with_appcontext

import uuid
import json


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


def parse_investment_data(investment_data_file):
    with open(investment_data_file) as f:
        investment_data = json.load(f)

    return investment_data


def populate_db(investment_data):
    for company in investment_data['companies']:
        add_company(
            company['name'],
            company['city']
        )

    for investor in investment_data['investors']:
        add_investor(
            investor['name'],
            investor['city']
        )

    for investment in investment_data['investments']:
        add_investment(
            investment['company'],
            investment['investors'],
            investment['investment stage'],
            investment['round size'],
            investment['date']
        )


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as schema_file:
        db.executescript(schema_file.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

    investment_data_file = current_app.config['INVESTMENT_DATA']
    investment_data = parse_investment_data(investment_data_file)
    click.echo('Loaded investement data.')
    populate_db(investment_data)
    click.echo('Populated the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
