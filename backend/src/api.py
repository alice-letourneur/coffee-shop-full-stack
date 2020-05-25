import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

## ROUTES
@app.route('/drinks')
def get_drinks():
    return jsonify(
        {
            'success': True,
            'drinks': [drink.short() for drink in Drink.query.all()]
        }
    )

@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(token):
    return jsonify(
        {
            'success': True,
            'drinks': [drink.long() for drink in Drink.query.all()]
        }
    )

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(token):
    try:
        body = request.get_json()
        drink = Drink(
            title=body.get('title'),
            recipe=json.dumps(body.get('recipe')),
        )
        drink.insert()

        return jsonify(
        {
            'success': True,
            'drinks': [drink.long()],
        }
        )
    except:
        abort(422)

@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(token, id):
    drink = Drink.query.get(id)
    if not drink:
        abort(404)

    try:
        body = request.get_json()
        title = body.get('title', None)
        recipe = body.get('recipe', None)

        if title:
            drink.title = body.get('title')

        if recipe:
            drink.recipe = json.dumps(recipe)

        if title or recipe:
            drink.update()

        return jsonify(
            {
                'success': True,
                'drinks': [drink.long()],
            }
        )
    except:
        abort(422)

@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(token, id):
    drink = Drink.query.get(id)

    if not drink:
        abort(404)

    try:
        drink.delete()

        return jsonify(
            {
            'delete': id,
            'success': True,
            }
        )
    except:
        abort(422)


## Error Handling

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found",
    }), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request",
    }), 400

@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Method not allowed",
    }), 405

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
