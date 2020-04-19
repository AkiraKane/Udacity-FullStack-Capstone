import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://{}@{}/{}".format(
            "akira", 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Creating a test for the /movies GET endpoint
    def test_200_get_movies(self):
        # Retrieving information from endpoint
        res = self.client().get('/movies')
        # Transforming body response into JSON
        data = json.loads(res.data)

        # Asserting that tests are valid
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # Creating a test not found for the /movies GET endpoint
    def test_404_get_movies(self):
        # Retriving information from the endpoint
        res = self.client().get('/moviess')
        # Transforming body response into JSON
        data = json.loads(res.data)

        # Asserting that tests are valid
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

        # Creating a test for the /actors GET endpoint
    def test_200_get_actors(self):
        # Retrieving information from endpoint
        res = self.client().get('/actors')
        # Transforming body response into JSON
        data = json.loads(res.data)

        # Asserting that tests are valid
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # Creating a test not found for the /actors GET endpoint
    def test_404_get_actors(self):
        # Retriving information from the endpoint
        res = self.client().get('/acters')
        # Transforming body response into JSON
        data = json.loads(res.data)

        # Asserting that tests are valid
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # Creating a test for the /movies POST endpoint
    def test_200_post_movies(self):
        # Posting dummy movie data to movies POST endpoint
        res = self.client().post(
            '/movies', json={"title": "Boss Level", "release_year": 2020})
        # Transforming body response into JSON
        data = json.loads(res.data)

        # Asserting that tests are valid
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # Creating a test unprocessable for the /movies POST endpoint
    def test_422_post_movies(self):
        # Posting incomplete dummy movie data to the movies POST endpoint
        res = self.client().post(
            '/movies',
            json={'title': 'Boss Level'})
        # Transforming body response into JSON
        data = json.loads(res.data)

        # Asserting that tests are valid
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable')

        # Creating a test for the /actors POST endpoint
    def test_200_post_actors(self):
        # Posting dummy movie data to actors POST endpoint
        res = self.client().post('/actors', json={"name": "Mel Gibson",
                                                  'age': 64, 'gender': "male", 'movie_id': 1})
        # Transforming body response into JSON
        data = json.loads(res.data)

        # Asserting that tests are valid
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # Creating a test unprocessable for the /actors POST endpoint
    def test_422_post_actors(self):
        # Posting incomplete dummy actor data to the actors POST endpoint
        res = self.client().post(
            '/actors',
            json={"name": "Mel Gibson"})
        # Transforming body response into JSON
        data = json.loads(res.data)

        # Asserting that tests are valid
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable')

     # Creating a test for the /movies PATCH endpoint
    def test_200_update_movies(self):
        # Calling patch endpoint with valid movie_id
        res = self.client().patch(
            '/movies/1', json={'title': 'Braveheart'})
        # Transforming body response into JSON
        data = json.loads(res.data)

        # Asserting that tests are valid
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # Creating a test not found for the /movies PATCH endpoint
    def test_404_update_movies(self):
        # Calling patch endpoint with invalid movie_id
        res = self.client().patch('/movies/100',
                                  json={'title': 'Braveheart'})
        # Transforming body response into JSON
        data = json.loads(res.data)

        # Asserting that tests are valid
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # Creating a test for the /actors PATCH endpoint
    def test_200_update_actors(self):
        # Calling patch endpoint with valid actor_id
        res = self.client().patch(
            '/actors/1', json={'name': 'Frank Grillo'})
        # Transforming body response into JSON
        data = json.loads(res.data)

        # Asserting that tests are valid
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # Creating a test not found for the /actors PATCH endpoint
    def test_404_update_actors(self):
        # Calling patch endpoint with invalid actor_id
        res = self.client().patch('/actors/100', json={'name': 'Frank Grillo'})
        # Transforming body response into JSON
        data = json.loads(res.data)

        # Asserting that tests are valid
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # Creating a test for the /movies DELETE endpoint

    def test_200_delete_movies(self):
        # Calling delete endpoint with valid movie_id
        res = self.client().delete('/movies/1')
        # Transforming body response into JSON
        data = json.loads(res.data)

        # Asserting that tests are valid
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    # Creating a test not found for the /movies DELETE endpoint
    def test_404_delete_movies(self):
        # Calling delete endpoint with invalid movie_id
        res = self.client().delete('/movies/100')
        # Transforming body response into JSON
        data = json.loads(res.data)

        # Asserting that tests are valid
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # Creating a test for the /actors DELETE endpoint
    def test_200_delete_actors(self):
        # Calling delete endpoint with valid actor_id
        res = self.client().delete('/actors/1')
        # Transforming body response into JSON
        data = json.loads(res.data)

        # Asserting that tests are valid
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])

    # Creating a test not found for the /actors DELETE endpoint
    def test_404_delete_actors(self):
        # Calling delete endpoint with invalid actor_id
        res = self.client().delete('/actors/100')
        # Transforming body response into JSON
        data = json.loads(res.data)

        # Asserting that tests are valid
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
