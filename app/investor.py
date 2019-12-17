import json
from flask import (
    Blueprint, request, jsonify
)
from app.db import query_db

bp = Blueprint('investor', __name__, url_prefix='/investor')


@bp.route('/')
def get_all_investors():
    investors = query_db('SELECT * from investor')

    return jsonify(investors)


@bp.route('/<name>')
def get_investors_with_name(name):
    investor = query_db('SELECT * from investor WHERE name = ?', args=(name,))

    return jsonify(investor)

@bp.route('/<name>/company')
def get_companies_for_investor_with_name(name):
    '''Get the names of all companies the investor invested in'''

    investors = query_db(
        '''
        SELECT company from investment_round
            JOIN investment ON investment_round.id = investment.investment_round_id
            JOIN investor on investment.investor = investor.name
        WHERE investor = ?
        GROUP BY id
        ''',
        args=(name,)
    )

    return jsonify(investors)

@bp.route('/<name>/investment')
def get_investments_for_investor_with_name(name):
    '''Get all investments and total investent round amount for investor'''

    investments = query_db(
        '''
        SELECT
            id,
            company,
            date,
            investment_stage,
            investor,
            round_size
        FROM investment_round
            JOIN investment ON investment_round.id = investment.investment_round_id
        WHERE investor = ?
        GROUP BY id
        ''',
        args=(name,)
    )

    response = {
        'investments': investments,
        'total': {
            'number_of_investments': len(investments),
            'amount_of_rounds': sum([investment['round_size'] for investment in investments])
        }
    }

    return response
