import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db


class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "example"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.producer_headers = {
            "Content-Type": "application/json",
            "Authorization":  os.environ.get('EXECUTIVE_PRODUCER')
        }
        self.assistant_headers = {
            "Content-Type": "application/json",
            "Authorization":  os.environ.get('CASTING_ASSISTANT')
        }

        self.new_actor = {
            'name': 'karim',
            'age': 23,
            'gender': 'male'
        }
        self.new_movie = {
            'title': 'Avengers4'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    ###########
    # Test Actor get
    ###################
    def test_get_all_actors(self):
        res = self.client().get(
            '/actors', headers={"Authorization": "Bearer {}".
                                format(self.producer_headers)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["actors"]))

    def test_401_get_actors_error(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unauthorized Error")

    ###############
    # Test Movie Get
    ##################
    def test_get_all_movies(self):
        res = self.client().get(
            '/movies', headers={"Authorization": "Bearer {}".
                                format(self.producer_headers)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))

    def test_401_get_movies_error(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unauthorized Error")

    ###################
    # Test Post Actor
    ###################
    def test_create_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers={"Authorization": "Bearer {}".
                                          format(self.producer_headers)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data['actors']))

    def test_401_create_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unauthorized Error")

    ###################
    # Test Post Moive
    ###################
    def test_create_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers={"Authorization": "Bearer {}".
                                          format(self.producer_headers)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data['movies']))

    def test_401_create_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unauthorized Error")
    ###################
    # Test Patch Actor
    ###################

    def test_update_actor(self):
        self.client().post('/actors', json=self.new_actor,
                           headers=self.producer_headers)
        res = self.client().patch('/actors/4', json={'name': 'ahmed',
                                                     'age': 25,
                                                     'gender': 'male'},
                                  headers={"Authorization": "Bearer {}".
                                           format(self.producer_headers)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data['actors']))

    def test_404_update_actor(self):
        res = self.client().patch('/actors/100', json={'name': 'ahmed',
                                                       'age': 25,
                                                       'gender': 'male'},
                                  headers={"Authorization": "Bearer {}".
                                           format(self.producer_headers)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")
        self.assertTrue(len(data['actors']))

    ###################
    # Test Patch Movie
    ###################

    def test_update_movie(self):
        self.client().post('/movies', json=self.new_movie,
                           headers=self.producer_headers)
        res = self.client().patch(
            '/movies/5', json={'title': 'Avenger2'},
            headers={"Authorization": "Bearer {}".
                     format(self.producer_headers)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data['movies']))

    def test_404_update_movie(self):
        res = self.client().patch(
            '/movies/100', json={'title': 'X-Men'},
            headers={"Authorization": "Bearer {}".
                     format(self.producer_headers)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")
        self.assertTrue(len(data['movies']))
    ###################
    # Test Delete Actor
    ###################

    def test_delete_actor(self):
        self.client().post('/actors', json=self.new_actor,
                           headers=self.producer_headers)
        self.client().post('/actors', json=self.new_actor,
                           headers=self.producer_headers)
        res = self.client().delete('/actors/2',
                                   headers={"Authorization": "Bearer {}".
                                            format(self.producer_headers)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data['actors']))

    def test_404_delete_actor(self):
        res = self.client().delete('/actors/50',
                                   headers={"Authorization": "Bearer {}".
                                            format(self.producer_headers)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")
        self.assertTrue(len(data['actors']))

    ###################
    # Test Delete Movie
    ###################

    def test_delete_movie(self):
        self.client().post('/movies', json=self.new_actor,
                           headers=self.producer_headers)
        self.client().post('/movies', json=self.new_actor,
                           headers=self.producer_headers)
        res = self.client().delete('/movies/2',
                                   headers={"Authorization": "Bearer {}".
                                            format(self.producer_headers)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data['movies']))

    def test_404_delete_movie(self):
        res = self.client().delete('/movies/50',
                                   headers={"Authorization": "Bearer {}".
                                            format(self.producer_headers)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")
        self.assertTrue(len(data['movies']))

    ################
    # Test for assitant
    # Test Actor get
    ###################
    def test_get_all_actors_assistant(self):
        res = self.client().get(
            '/actors', headers={"Authorization": "Bearer {}".
                                format(self.assistant_headers)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["actors"]))

    def test_401_get_actors_error_assistant(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unauthorized Error")

    ###############
    # Test Movie Get
    ##################
    def test_get_all_movies_assistant(self):
        res = self.client().get(
            '/movies', headers={"Authorization": "Bearer {}".
                                format(self.assistant_headers)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))

    def test_401_get_movies_error_assistant(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unauthorized Error")
        
# Make the tests conveniently executable
if __name__ == "__main__":
  unittest.main()