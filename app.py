from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from models import setup_db, Actor, Movie, db, db_drop_and_create_all
from auth import AuthError, requires_auth


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={"/": {"origins": "*"}})

    # Uncomment this line for the first time use only.
    # db_drop_and_create_all()

    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers",
                             "Content-Type, Authorization, true")
        response.headers.add("Access-Control-Allow-Methods",
                             "GET, PATCH, POST, DELETE, OPTIONS")
        return response

    #################################### Public Endpoint ############################

    """
    A public endpoint for checking if site is working
    """
    @app.route('/')
    def check_url():
        greeting = "Hi there, the app is running"
        return jsonify({
            "success": True,
            "message": greeting
        })

    #################################### Private Endpoints ###########################

    """
    A private endpoint for getting all actors
    """
    @app.route('/actors')
    @requires_auth("get:actors")
    def get_actors(payload):

        # retrieve all actors from db
        actors_db = Actor.query.order_by(Actor.id).all()

        # abort 404 if no actors found
        if len(actors_db) == 0:
            abort(404)

        # format the actors
        actors = [actor.format() for actor in actors_db]

        # return status code 200 and json file where actors is the list of formatted actors
        return jsonify({
            "success": True,
            "actors": actors
        })

    """
    A private endpoint for getting all movies
    """
    @app.route('/movies')
    @requires_auth("get:movies")
    def get_movies(payload):

        # retrieve all movies from db
        movies_db = Movie.query.order_by(Movie.id).all()

        # abort 404 if no movies found
        if len(movies_db) == 0:
            abort(404)

        # format the movies
        movies = [movie.format() for movie in movies_db]

        # return status code 200 and json file where movies is the list of formatted movies
        return jsonify({
            "success": True,
            "movies": movies
        })

    """
    A private endpoint for posting actors
    """
    @app.route("/actors", methods=["POST"])
    @requires_auth("post:actors")
    def post_actors(payload):

        # retrieve data fields from the request body
        body = request.get_json()

        new_name = body.get("name", None)
        new_age = body.get("age", None)
        new_gender = body.get("gender", None)
        new_movie_id = body.get("movie_id", None)

        # abort 422 if any field is blank
        if not (new_name and new_age and new_gender and new_movie_id):
            abort(422)

        # try to add the new data into db
        new_actor = Actor(name=new_name,
                          age=new_age,
                          gender=new_gender,
                          movie_id=new_movie_id)

        try:
            new_actor.insert()

        # abort 422 if any error
        except Exception as e:
            print("Error: ", str(e))
            abort(422)

        # returns status code 200 and json file where actors
        # is an array containing only the newly created actor
        return jsonify({
            "success": True,
            "actors": [new_actor.format()]
        })

    """
    A private endpoint for posting movies
    """
    @app.route("/movies", methods=["POST"])
    @requires_auth("post:movies")
    def post_movies(payload):

        # retrieve data fields from the request body
        body = request.get_json()

        new_title = body.get("title", None)
        new_release_year = body.get("release_year", None)

        # abort 422 if any field is blank
        if not new_title or not new_release_year:
            abort(422)

        # try to add the new data into db
        new_movie = Movie(title=new_title,
                          release_year=new_release_year)

        try:
            new_movie.insert()

        # abort 422 if any error
        except Exception as e:
            print("Error: ", str(e))
            abort(422)

        # returns status code 200 and json file where movie
        # is an array containing only the newly created movie
        return jsonify({
            "success": True,
            "movies": [new_movie.format()]
        })

    """
    A private endpoint for patching a actor by a given id
    """
    @app.route("/actors/<int:id>", methods=["PATCH"])
    @requires_auth("patch:actors")
    def update_actors(*args, **kwargs):

        # get id from kwargs
        id = kwargs["id"]

        # get actor by a given id
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        # abort 404 if no actor found
        if actor is None:
            abort(404)

        # retrieve data fields from the request body
        body = request.get_json()

        if "name" in body:
            actor.name = body.get("name")

        if "age" in body:
            actor.age = body.get("age")

        if "gender" in body:
            actor.gender = body.get("gender")

        if "movie_id" in body:
            actor.movie_id = body.get("movie_id")

        # update new data in db
        try:
            actor.update()

        # abort 422 if any error
        except Exception as e:
            print("Error: ", str(e))
            abort(422)

        # returns status code 200 and json file where actors
        # is an array containing only the newly modified actor
        return jsonify({
            "success": True,
            "actors": [actor.format()]
        })

    """
    A private endpoint for patching a movie by a given id
    """
    @app.route("/movies/<int:id>", methods=["PATCH"])
    @requires_auth("patch:movies")
    def update_movies(*args, **kwargs):

        # get id from kwargs
        id = kwargs["id"]

        # get movie by a given id
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        # abort 404 if no movie found
        if movie is None:
            abort(404)

        # retrieve data fields from the request body
        body = request.get_json()

        if "title" in body:
            movie.title = body.get("title")

        if "release_year" in body:
            movie.release_year = body.get("release_year")

        # update new data in db
        try:
            movie.update()

        # abort 422 if any error
        except Exception as e:
            print("Error: ", str(e))
            abort(422)

        # returns status code 200 and json file where movies
        # is an array containing only the newly modified movie
        return jsonify({
            "success": True,
            "movies": [movie.format()]
        })

    """
    A private endpoint for deleting a actor by given id
    """
    @app.route("/actors/<int:id>", methods=["DELETE"])
    @requires_auth("delete:actors")
    def delete_actors(*args, **kwargs):

        # get id from kwargs
        id = kwargs["id"]

        # get actor by a given id
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        # abort 404 if no actor found
        if actor is None:
            abort(404)

        # deletr data from db
        try:
            actor.delete()

        # abort 422 if any error
        except Exception as e:
            print("Error: ", str(e))
            abort(422)

        # returns status code 200 and json file where deleted
        # is the id of deleted actor
        return jsonify({
            "success": True,
            "deleted": id
        })

    """
    A private endpoint for deleting a movie by given id
    """
    @app.route("/movies/<int:id>", methods=["DELETE"])
    @requires_auth("delete:movies")
    def delete_movies(*args, **kwargs):

        # get id from kwargs
        id = kwargs["id"]

        # get movie by a given id
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        # abort 404 if no movie found
        if movie is None:
            abort(404)

        # deletr data from db
        try:
            movie.delete()

        # abort 422 if any error
        except Exception as e:
            print("Error: ", str(e))
            abort(422)

        # returns status code 200 and json file where deleted
        # is the id of deleted actor
        return jsonify({
            "success": True,
            "deleted": id
        })

    ###################################### Error Handling ######################################
    '''
    Error handling for unprocessable entity
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    '''
    Error handling for resource not found 
    '''
    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    '''
    Error handler for AuthError
    '''
    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        response = jsonify(ex.error)
        response.status_code = ex.status_code
        return response

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
