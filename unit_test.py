import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import setup_db, Movie, Actor, db


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "casting-agency"
        self.database_path = "postgres://postgres:stemed@{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.casting_assistant_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZaY0JqX2UxeWlPM29yLV9qTVhyMyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjYS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDMwMjEyNTk5MDM1OTgxMjM1MzUiLCJhdWQiOlsiY2FzdGluZyBhZ2VuY3kiLCJodHRwczovL2ZzbmRjYS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTg2MTg2MDkwLCJleHAiOjE1ODYxOTMyOTAsImF6cCI6IllBWlhncWpoQ0NPQ3c1RUlnNHhsUWVYdWtlTktrQm1yIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.WCrehhag0pcCn_BJlNwBygQ4HubUsJdYGF99b7a1MmrjSlfoU3D1CXqfrEEAMiKJqVWjfJPbtiVo7JX8wwaK9LckHt0R1TZl39_bkwhwwuqE_ZOAfv29LXij0oswUBvCgdwOEw8D-cnxwYIO5fTNKs_4uFu_0S7bmYWwA2F95-3eucJAkiKufCxDonv1qztZ4PcnhACq7zGBujjG4-G5PQ04uNGzaDkFALnaxvjzhUT-SX-2zBgpdjUHs-Rg4JD4OVTR2KPzLiPbo_-kArv1kIFtGi8R5US8sYbJzqr53rPRJgNb004GvfR-QYwU2m-QR6GD0ZMrAISzJOEBXccCUA'
        }

        self.casting_director_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZaY0JqX2UxeWlPM29yLV9qTVhyMyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjYS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDMyMzU5MTE1NDgzMjg3NjU2MTIiLCJhdWQiOlsiY2FzdGluZyBhZ2VuY3kiLCJodHRwczovL2ZzbmRjYS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTg2MTg2Mjg5LCJleHAiOjE1ODYxOTM0ODksImF6cCI6IllBWlhncWpoQ0NPQ3c1RUlnNHhsUWVYdWtlTktrQm1yIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.3nrKjzn-G9OApHB7JPau00yXMVUpEAIgcTUtSJE6HxUlNTWMMklK2PD7p7qIjGhVGOp2_Vq_-RXAj146Rno7P7xNTfqeJrsn53aPVHpUDC1iIqUWdxLN1JBYcR6ebz6QaLUKElJZ_mjW2Dvk6dBcBwkTmG5OqrPXpA__oQhaxSh8XhNDYP6RLSjtoLVBUsp7yyAdPj7VMHF9Z4g-RXYPxSaJ7ahkc9VpKPXemVyNPMyCM-tZ3eM5UNHsUIiIpKBu65MHrPPAL7CRScMIQdZ-2bw1J2wUQ6Sgb_VrMIFUS4UPJVACK90BLwhFn95FyPrCE10_OjKH8NqUA3ubsxGErg'
        }

        self.executive_producer_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZaY0JqX2UxeWlPM29yLV9qTVhyMyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjYS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTI2OTIyODc1OTYxOTA3NTA0MDMiLCJhdWQiOlsiY2FzdGluZyBhZ2VuY3kiLCJodHRwczovL2ZzbmRjYS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTg2MTg2MjE2LCJleHAiOjE1ODYxOTM0MTYsImF6cCI6IllBWlhncWpoQ0NPQ3c1RUlnNHhsUWVYdWtlTktrQm1yIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.uh3Ju9z0ZEykXAO7_8-qxvx5Lrg_2XSLRzCGxMVrtGGiXCNCAV0OtzFbHjvngrMda4xomVpgsxY42aYdXULwd8U31q2ftnDwkMVNZc8DnRtlX6gJAFdEl1baGAwkyu4osNCeVbSCtX7v7VC7Ky3bwLmq_CB1sRqhqvh_AmY3LRrUp7VS749zxd53Th1HTZz9JEBMp9boG5y7C0lm6Q2jcYt_ssmjGTPWXhK_A6XfpolR_-2vFZvQ9VFpbqdjfpXOfLGtwkE75Ml1es5NUd2tdTfJPXWI6RZvTMx3v7oqDEpcFmzIbw1aWWPKTBvn8HFRpq8baU82iYfGtD0q4aAS2g'
        }

        self.movie = {
            'title': 'Hello Brother',
            'release_date': '3011'
        }

        self.new_movie = {
            'title': 'Coolie No 1',
            'release_date': '1011'
        }

        self.actor = {
            'name': 'Deepika Padukone',
            'age': '30',
            'gender': 'Female'
        }

        self.new_actor = {
            'name': 'Govinda',
            'age': '40',
            'gender': 'Male'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = db
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # Seed test data
        self.client().post('/movies', json=self.movie,
                           headers=self.executive_producer_header)
        self.client().post('/actors', json=self.actor,
                           headers=self.executive_producer_header)

    def tearDown(self):
        """Executed after reach test"""
        self.db.drop_all()
        pass

    # Test GET Actors
    def test_get_actors_public(self):
        res = self.client().get('/actors')

        self.assertEqual(res.status_code, 401)

    def test_get_actors_casting_assistant(self):
        res = self.client().get('/actors',
                                headers=self.casting_assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_get_actors_casting_director(self):
        res = self.client().get('/actors',
                                headers=self.casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    def test_get_actors_executive_producer(self):
        res = self.client().get('/actors',
                                headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['actors']))

    # Test GET Movies
    def test_get_movies_public(self):
        res = self.client().get('/movies')

        self.assertEqual(res.status_code, 401)

    def test_get_movies_casting_assistant(self):
        res = self.client().get('/movies',
                                headers=self.casting_assistant_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_get_movies_casting_director(self):
        res = self.client().get('/movies',
                                headers=self.casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    def test_get_movies_executive_producer(self):
        res = self.client().get('/movies',
                                headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['movies']))

    # Test POST Actor
    def test_post_actors_public(self):
        res = self.client().post('/actors', json=self.new_actor)

        self.assertEqual(res.status_code, 401)

    def test_post_actors_casting_assistant(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers=self.casting_assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_post_actors_casting_director(self):
        original_count = len(Actor.query.all())

        res = self.client().post('/actors', json=self.new_actor,
                                 headers=self.casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertGreater(data['id'], 0)

    def test_post_actors_executive_producer(self):
        original_count = len(Actor.query.all())

        res = self.client().post('/actors', json=self.new_actor,
                                 headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertGreater(data['id'], 0)

    # Test POST Movie
    def test_post_movies_public(self):
        res = self.client().post('/movies', json=self.new_movie)

        self.assertEqual(res.status_code, 401)

    def test_post_movies_casting_assistant(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=self.casting_assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_post_movies_casting_director(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=self.casting_director_header)

        self.assertEqual(res.status_code, 401)

    def test_post_movies_executive_producer(self):
        original_count = len(Movie.query.all())

        res = self.client().post('/movies', json=self.new_movie,
                                 headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertGreater(data['id'], 0)

    # Test PATCH Actor
    def test_patch_actors_public(self):
        res = self.client().patch('/actors/1', json={'age': "43"})

        self.assertEqual(res.status_code, 401)

    def test_patch_actors_casting_assistant(self):
        res = self.client().patch(
            '/actors/1', json={'age': "43"},
            headers=self.casting_assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_patch_actors_casting_director(self):
        res = self.client().patch(
            '/actors/1', json={'age': "43"},
            headers=self.casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actors_executive_producer(self):
        res = self.client().patch(
            '/actors/1', json={'age': "43"},
            headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actors_does_not_exist(self):
        res = self.client().patch(
            '/actors/1000', json={'age': "43"},
            headers=self.executive_producer_header)

        self.assertEqual(res.status_code, 404)

    def test_patch_actors_no_data(self):
        res = self.client().patch('/actors/1',
                                  headers=self.executive_producer_header)

        self.assertEqual(res.status_code, 422)

    # Test PATCH Movie
    def test_patch_movies_public(self):
        res = self.client().patch('/movies/1', json={'title': "Updated Title"})

        self.assertEqual(res.status_code, 401)

    def test_patch_movies_casting_assistant(self):
        res = self.client().patch('/movies/1',
                                  json={'title': "Updated Title"},
                                  headers=self.casting_assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_patch_movies_casting_director(self):
        res = self.client().patch('/movies/1',
                                  json={'title': "Updated Title"},
                                  headers=self.casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movies_executive_producer(self):
        res = self.client().patch('/movies/1',
                                  json={'title': "Updated Title"},
                                  headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movies_does_not_exist(self):
        res = self.client().patch('/movies/1000',
                                  json={'title': "Updated Title"},
                                  headers=self.executive_producer_header)

        self.assertEqual(res.status_code, 404)

    def test_patch_movies_no_data(self):
        res = self.client().patch('/movies/1',
                                  headers=self.executive_producer_header)

        self.assertEqual(res.status_code, 422)

    # Test DELETE Actor
    def test_delete_actors_public(self):
        res = self.client().delete('/actors/1')

        self.assertEqual(res.status_code, 401)

    def test_delete_actors_casting_assistant(self):
        res = self.client().delete('/actors/1',
                                   headers=self.casting_assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_delete_actors_casting_director(self):
        res = self.client().delete('/actors/1',
                                   headers=self.casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actors_executive_producer(self):
        res = self.client().delete('/actors/1',
                                   headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actors_does_not_exist(self):
        res = self.client().delete('/actors/1000',
                                   headers=self.executive_producer_header)

        self.assertEqual(res.status_code, 404)

    # Test DELETE Movie
    def test_delete_movies_public(self):
        res = self.client().delete('/movies/1')

        self.assertEqual(res.status_code, 401)

    def test_delete_movies_casting_assistant(self):
        res = self.client().delete('/movies/1',
                                   headers=self.casting_assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_delete_movies_casting_director(self):
        res = self.client().delete('/movies/1',
                                   headers=self.casting_director_header)

        self.assertEqual(res.status_code, 401)

    def test_delete_movies_executive_producer(self):
        res = self.client().delete('/movies/1',
                                   headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],
                         True)

    def test_delete_movies_does_not_exist(self):
        res = self.client().delete('/movies/1000',
                                   headers=self.executive_producer_header)

        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
