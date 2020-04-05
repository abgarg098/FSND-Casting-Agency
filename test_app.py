import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import APP
from models import setup_db, Movie, Actor, db

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = APP
        self.client = self.app.test_client
        self.database_name = "casting-agency"
        self.database_path = "postgres://postgres:stemed@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.casting_assistant_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFqSkROVEpGT0VRNU5rRkJNamd3TWpCR1JqQTNNakZDT0RWRFFqWTVOREUwTXpVMU1EVTROQSJ9.eyJpc3MiOiJodHRwczovL3N0ZW1lZC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUzOWFmZjg0ZmNmMzIwY2FhOWNhMTFhIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4NDU0NTkyMSwiZXhwIjoxNTg0NjMyMzIxLCJhenAiOiJlNklralk3V29qcXpTY3htMUlsUTRJZU1na1puS2xGMyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.Nwcs18JyIoSVCfRAqO0wZc3Dv456g-0BXSh58fi9rsqNvIKD1oovCN3UzFFdo70b85s1hxaZGLlJ0pynWrxkQS0Wv9w1ip0Kwz8XC_2XPIx9FFFBjFfVM0jSQOdWAfw7X39nDJ1fixlzeqxdZUKxuq5KuHsVx2xKvjfCLzkRe9X-drp2wamoEaVFZpP2KIXwAthejS6wpo7pqA6EgvAi-Hb1ciZ6_rsDoVAqL5b1jOQqON-NDWq01hRPw3g4qDGd9_DzeKyc3SsXRghzc4t0z1Sw_wBzBGKtglY-Lsi_815580Fc0IBXYm37oKZDgT9s79CRq6ivFjdzXS8dpBFIJw'
        }

        self.casting_director_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFqSkROVEpGT0VRNU5rRkJNamd3TWpCR1JqQTNNakZDT0RWRFFqWTVOREUwTXpVMU1EVTROQSJ9.eyJpc3MiOiJodHRwczovL3N0ZW1lZC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU2YzE3MzUyYWU2YTgwYzhiYzI0NmUwIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4NDU0NjAyOCwiZXhwIjoxNTg0NjMyNDI4LCJhenAiOiJlNklralk3V29qcXpTY3htMUlsUTRJZU1na1puS2xGMyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciJdfQ.BeOgv6OVDSpztMgTKeTZTG6bbG639f2z9hdW7zeO4tuGRhQjt9Zm9XS76YXnr6TwnVkidNDsG2r1_zy5a7WnZRfYY32OQPxnUk7AVaxsDTrLLppwFXpoRKlPY21Cvu7zrYqGAEyvND9lGbDfbI1D4QvXQoDIs6wq-lNjSuJ82yIaceRpWA-ZWXCaqB5f9WQVVPwwlqO_XYrOThJMl2evHik3mdFVy8bZxEAzqEpBcxGdHOU3ZoJPwnNdMTgd-UvnQCrWK2wQsCNV3Z6ucWfyy6eA6xZ8qMi7rM_GybZ1xeRIEtMe1eOoHzonFaHiiKrJwbDg4XbNFuqemPBkLOZwdw'
        }

        self.executive_producer_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlFqSkROVEpGT0VRNU5rRkJNamd3TWpCR1JqQTNNakZDT0RWRFFqWTVOREUwTXpVMU1EVTROQSJ9.eyJpc3MiOiJodHRwczovL3N0ZW1lZC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWUyZjc1NTZiOGRhMjEwZTZlOWRlNmRjIiwiYXVkIjoiY2FzdGluZyIsImlhdCI6MTU4NDU0NTY2MSwiZXhwIjoxNTg0NjMyMDYxLCJhenAiOiJlNklralk3V29qcXpTY3htMUlsUTRJZU1na1puS2xGMyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.H9K5MvZt4H1fQLRoxXovsBM6W3l3mcAYZfoP8I_Z8qQx7oUcT_OJbTu9QyOtCJ2hKo6sWW_FuUk0TYiWIqy5FcaZm0cLGOi1hSwGMYdOUS0YtHH0lc_3YxicVXZG0Hp_25S1z5sJjwbdQLV2uzs21oq73gMB7l32IVgvy02Qn3WPWnDLW745pvFLGwl_38hTGnhpYLyKAtfX9jdUFdzKWWbYqGQ5JxSIRskBrs0sN51ef7cvbeqX-hJ4WU36CGyNMa7GVA1RH2IxEPYeGE19Mkd8573zUrZfqtyW3Jds0iFOkDrxK03lf4oq2j0m5hARKVMrgl6nSfxpAn18qnU5rQ'
        }

        self.movie = {
            'title': 'Avengers: Endgame',
            'release_date': '2019'
        }

        self.new_movie = {
            'title': 'Black Widow',
            'release_date': '2019'
        }

        self.actor = {
            'name': 'Scarlett Johansson',
            'age': '35',
            'gender': 'Female'
        }

        self.new_actor = {
            'name': 'Robert Downey Jr.',
            'age': '54',
            'gender': 'Male'
        }


        # binds the app to the current context
        with self.app.app_context():
            self.db = db
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        #Seed test data
        self.client().post('/movies', json=self.movie, headers=self.executive_producer_header)
        self.client().post('/actors', json=self.actor, headers=self.executive_producer_header)  

    def tearDown(self):
        """Executed after reach test"""
        self.db.drop_all()
        pass

    # Test GET Actors
    def test_get_actors_public(self):
        res = self.client().get('/actors')

        self.assertEqual(res.status_code, 401)

    def test_get_actors_casting_assistant(self):
        res = self.client().get('/actors', headers=self.casting_assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_get_actors_casting_director(self):
        res = self.client().get('/actors', headers=self.casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_get_actors_executive_producer(self):
        res = self.client().get('/actors', headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    # Test GET Movies
    def test_get_movies_public(self):
        res = self.client().get('/movies')

        self.assertEqual(res.status_code, 401)

    def test_get_movies_casting_assistant(self):
        res = self.client().get('/movies', headers=self.casting_assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_get_movies_casting_director(self):
        res = self.client().get('/movies', headers=self.casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_get_movies_executive_producer(self):
        res = self.client().get('/movies', headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    # Test POST Actor
    def test_post_actors_public(self):
        res = self.client().post('/actors', json=self.new_actor)

        self.assertEqual(res.status_code, 401)

    def test_post_actors_casting_assistant(self):
        res = self.client().post('/actors', json=self.new_actor, headers=self.casting_assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_post_actors_casting_director(self):
        original_count = len(Actor.query.all())

        res = self.client().post('/actors', json=self.new_actor, headers=self.casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertGreater(data['id'], 0)

    def test_post_actors_executive_producer(self):
        original_count = len(Actor.query.all())

        res = self.client().post('/actors', json=self.new_actor, headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertGreater(data['id'], 0)

    # Test POST Movie
    def test_post_movies_public(self):
        res = self.client().post('/movies', json=self.new_movie)

        self.assertEqual(res.status_code, 401)

    def test_post_movies_casting_assistant(self):
        res = self.client().post('/movies', json=self.new_movie, headers=self.casting_assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_post_movies_casting_director(self):
        res = self.client().post('/movies', json=self.new_movie, headers=self.casting_director_header)

        self.assertEqual(res.status_code, 401)

    def test_post_movies_executive_producer(self):
        original_count = len(Movie.query.all())

        res = self.client().post('/movies', json=self.new_movie, headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertGreater(data['id'], 0)

    # Test PATCH Actor
    def test_patch_actors_public(self):
        res = self.client().patch('/actors/1', json={'age': "43"})

        self.assertEqual(res.status_code, 401)

    def test_patch_actors_casting_assistant(self):
        res = self.client().patch('/actors/1', json={'age': "43"}, headers=self.casting_assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_patch_actors_casting_director(self):
        res = self.client().patch('/actors/1', json={'age': "43"}, headers=self.casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actors_executive_producer(self):
        res = self.client().patch('/actors/1', json={'age': "43"}, headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actors_does_not_exist(self):
        res = self.client().patch('/actors/1000', json={'age': "43"}, headers=self.executive_producer_header)
        
        self.assertEqual(res.status_code, 404)

    def test_patch_actors_no_data(self):
        res = self.client().patch('/actors/1', headers=self.executive_producer_header)
        
        self.assertEqual(res.status_code, 404)

    # Test PATCH Movie
    def test_patch_movies_public(self):
        res = self.client().patch('/movies/1', json={'title': "Updated Title"})

        self.assertEqual(res.status_code, 401)

    def test_patch_movies_casting_assistant(self):
        res = self.client().patch('/movies/1', json={'title': "Updated Title"}, headers=self.casting_assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_patch_movies_casting_director(self):
        res = self.client().patch('/movies/1', json={'title': "Updated Title"}, headers=self.casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movies_executive_producer(self):
        res = self.client().patch('/movies/1', json={'title': "Updated Title"}, headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movies_does_not_exist(self):
        res = self.client().patch('/movies/1000', json={'title': "Updated Title"}, headers=self.executive_producer_header)
        
        self.assertEqual(res.status_code, 404)

    def test_patch_movies_no_data(self):
        res = self.client().patch('/movies/1', headers=self.executive_producer_header)
        
        self.assertEqual(res.status_code, 404)

    # Test DELETE Actor
    def test_delete_actors_public(self):
        res = self.client().delete('/actors/1')

        self.assertEqual(res.status_code, 401)

    def test_delete_actors_casting_assistant(self):
        res = self.client().delete('/actors/1', headers=self.casting_assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_delete_actors_casting_director(self):
        res = self.client().delete('/actors/1', headers=self.casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actors_executive_producer(self):
        res = self.client().delete('/actors/1', headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actors_does_not_exist(self):
        res = self.client().delete('/actors/1000', headers=self.executive_producer_header)
        
        self.assertEqual(res.status_code, 404)

    # Test DELETE Movie
    def test_delete_movies_public(self):
        res = self.client().delete('/movies/1')

        self.assertEqual(res.status_code, 401)

    def test_delete_movies_casting_assistant(self):
        res = self.client().delete('/movies/1', headers=self.casting_assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_delete_movies_casting_director(self):
        res = self.client().delete('/movies/1', headers=self.casting_director_header)

        self.assertEqual(res.status_code, 401)

    def test_delete_movies_executive_producer(self):
        res = self.client().delete('/movies/1', headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movies_does_not_exist(self):
        res = self.client().delete('/movies/1000', headers=self.executive_producer_header)
        
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()