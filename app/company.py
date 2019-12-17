import json
from flask import (
    Blueprint, request, jsonify
)
from app.db import query_db

bp = Blueprint('company', __name__, url_prefix='/company')


@bp.route('/')
def get_all_companies():
    companies = query_db('SELECT * from company')

    return jsonify(companies)


@bp.route('/<name>')
def get_companies_with_name(name):
    company = query_db('SELECT * from company WHERE name = ?', args=(name,))

    return jsonify(company)

@bp.route('/<name>/investor')
def get_investors_for_companies_with_name(name):
    '''Get the names of all investors in the company'''

    investors = query_db(
        '''
        SELECT investor from investment_round
            JOIN investment ON investment_round.id = investment.investment_round_id
            JOIN investor on investment.investor = investor.name
        WHERE company = ?
        GROUP BY id, investor
        ''',
        args=(name,)
    )

    return jsonify(investors)

@bp.route('/<name>/investment')
def get_investments_for_company(name):
    '''Get all investments and total investment amount for company'''

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
        WHERE company = ?
        GROUP BY id
        ''',
        args=(name,)
    )

    response = {
        'investments': investments,
        'total': {
            'number_of_investments': len(investments),
            'amount': sum([investment['round_size'] for investment in investments])
        }
    }

    return jsonify(response)
