import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import json
from flask_cors import CORS
from models import setup_db, Actor, Movie, db
from flask_migrate import Migrate
from auth import AuthError, requires_auth
RESULTS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # actor = Actor(name='ak', age=156, gender='sasaa')
    # movie = Movie(title='titanic2')
    # actor.actor_in_movies.append(movie)
    # db.session.add(actor)
    # db.session.commit()
    #########################
    # Get Actors
    #########################
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(token):
        try:
            actors_details = list(map(Actor.format, Actor.query.all()))
            result = {"success": True,
                      "actors": actors_details,
                      "total_actors": len(Actor.query.all()),
                      }
            return jsonify(result)
        except Exception:
            abort(404)

    ##########################
    # Get Movies
    ##########################
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(token):
        try:
            movies_details = list(map(Movie.format, Movie.query.all()))
            result = {"success": True,
                      "movies": movies_details,
                      "total_movies": len(Movie.query.all()),
                      }
            return jsonify(result)
        except Exception:
            abort(404)

    ############################
    # Delete Actor
    ############################
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(token, actor_id):
        try:

            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor is None:
                return 'No'

            actor.delete()
            return jsonify({
                "success": True,
                "message": "this actor id deleted",
                "delete": actor_id,
                "total_actors": len(Actor.query.all()),


            })
        except Exception:
            abort(422)
    #########################
    # Delete movie
    #########################

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(token, movie_id):
        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)

            movie.delete()
            return jsonify({
                "success": True,
                "message": "this movie id deleted",
                "delete": movie_id,
                "total_movies": len(Movie.query.all()),

            })
        except Exception:
            abort(422)

    ########################
    # Post actor
    ########################
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(token):
        body = request.get_json()
        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        if any(arg is None for arg in [new_name, new_age, new_gender])or'' in[new_name, new_age, new_gender]:
            abort(400)
        try:
            new_actor = Actor(name=new_name, age=new_age, gender=new_gender)
            new_actor.insert()
            return jsonify({
                "success": True,
                "created": new_actor.id,
            })
        except Exception:
            abort(422)
    #########################
    # Post actor
    ########################

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(token):
        body = request.get_json()
        new_title = body.get('title', None)

        if any(arg is None for arg in [new_title])or'' in[new_title]:
            abort(400)
        try:
            new_movie = Movie(title=new_title)
            new_movie.insert()
            return jsonify({
                "success": True,
                "created": new_movie.id,
            })
        except Exception:
            abort(422)

    ##########################
    # PATCH actor
    ##########################
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def edit_actor(token, actor_id):
        body = request.get_json()
        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        try:
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor is None:
                abort(404)
            if any(arg is None for arg in [new_name, new_age, new_gender])or'' in[new_name, new_age, new_gender]:
                abort(400)

            actor.name = new_name
            actor.age = new_age
            actor.gender = new_gender

            actor.update()
            return jsonify({
                "success": True,
                "actors": [Actor.query.get(actor_id).format()]
            })

        except Exception:
            abort(401)
    ##########################
    # PATCH movie
    ##########################

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movie(token, movie_id):
        body = request.get_json()
        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        try:
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)
            if any(arg is None for arg in [new_title])or'' in[new_title]:
                abort(400)

            movie.title = new_title
            movie.release_date = new_release_date

            movie.update()
            return jsonify({
                "success": True,
                "movie": [Movie.query.get(movie_id).format()]
            })

        except Exception:
            abort(401)

    #########################
    # Error Handling
    #########################
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
            "message": "Resource not found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad request"
        }), 400

    @app.errorhandler(401)
    def Unauthorized_error(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized Error "
        }), 401

    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


app = create_app()
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
