import click
import json

from flask.cli import with_appcontext
from flask import current_app

from app.db import (get_db, add_company, add_investor, add_investment)


def create_tables():
    db = get_db()

    with current_app.open_resource('schema.sql') as schema_file:
        db.executescript(schema_file.read().decode('utf8'))


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


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    create_tables()
    click.echo('Created the database tables.')

    investment_data_file = current_app.config['INVESTMENT_DATA']
    investment_data = parse_investment_data(investment_data_file)
    click.echo('Loaded investement data.')

    populate_db(investment_data)
    click.echo('Populated the database.')


def init_app(app):
    app.cli.add_command(init_db_command)
