import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, setup_db, Actor, Movie
from auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    return app


APP = create_app()

# if __name__ == '__main__':
#     APP.run(host='0.0.0.0', port=8080, debug=True)


@APP.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors(token):
    try:
        actors = Actor.query.order_by('id').all()

        if len(actors) == 0:
            raise AuthError(404)

        formatted_actors = [actor.format() for actor in actors]
        return jsonify({
            'actors': formatted_actors,
            'success': True
        }), 200

    except Exception:
        abort(422)


@APP.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies(token):
    try:
        movies = Movie.query.order_by('id').all()

        if len(movies) == 0:
            raise AuthError(404)

        formatted_movies = [movie.format() for movie in movies]
        return jsonify({
            'movies': formatted_movies,
            'success': True
        }), 200

    except Exception:
        abort(422)


@APP.route('/actors/<id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(token, id):
    actor = Actor.query.get(id)
    if actor is None:
        abort(404)

    body = request.get_json()
    if body is None:
        abort(422)

    try:
        if 'name' in body:
            actor.name = body['name']

        if 'age' in body:
            actor.age = body['age']

        if 'gender' in body:
            actor.gender = body['gender']

        actor.update()
        return jsonify({
            'success': True,
            'actors': [actor.format()]
        }), 200

    except Exception:
        abort(422)


@APP.route('/movies/<id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(token, id):
    movie = Movie.query.get(id)
    if movie is None:
        abort(404)

    body = request.get_json()
    if body is None:
        abort(422)

    try:
        if 'title' in body:
            movie.title = body['title']

        if 'release_date' in body:
            movie.release_date = body['release_date']

        movie.update()
        return jsonify({
            'success': True,
            'movies': [movie.format()]
        }), 200

    except Exception:
        abort(422)


@APP.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def add_actor(token):
    body = request.get_json()
    if body is None:
        abort(422)

    name = body.get('name', None)
    if name is None:
        abort(422)
    age = body.get('age', None)
    if age is None:
        abort(422)
    gender = body.get('gender', None)
    if gender is None:
        abort(422)

    try:
        new_actor = Actor(name=name, age=age, gender=gender)
        new_actor.insert()
        new_id = new_actor.id
        return jsonify({
            'id': new_id,
            'success': True
        }), 201

    except Exception:
        abort(422)


@APP.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def add_movie(token):
    body = request.get_json()
    if body is None:
        abort(422)

    title = body.get('title', None)
    if(title is None):
        abort(422)
    release_date = body.get('release_date', None)
    if(release_date is None):
        abort(422)

    try:
        new_movie = Movie(title=title, release_date=release_date)
        new_movie.insert()
        new_id = new_movie.id

        return jsonify({
            'id': new_id,
            'success': True
        }), 201

    except Exception:
        abort(422)


@APP.route('/actors/<id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(token, id):
    actor = Actor.query.get(id)

    if actor is None:
        abort(404)

    try:
        actor.delete()
        return jsonify({
            'success': True
        }), 200

    except Exception:
        abort(422)


@APP.route('/movies/<id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(token, id):
    movie = Movie.query.get(id)

    if movie is None:
        abort(404)

    try:
        movie.delete()

        return jsonify({
            'success': True
        }), 200

    except Exception:
        abort(422)


@APP.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
    }), 404


@APP.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@APP.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), error.status_code
