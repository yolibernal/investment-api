import json
from flask import (
    Blueprint, request, jsonify
)
from app.db import query_db

bp = Blueprint('investment', __name__, url_prefix='/investment')


@bp.route('/')
def get_all_investment_rounds():
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
        GROUP BY id
        '''
    )

    return jsonify(investments)


@bp.route('/<id>')
def get_investment_round_with_id(id):
    investment = query_db(
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
        WHERE id = ?
        GROUP BY id
        ''',
        args=(id,)
    )

    return jsonify(investment)
