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
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZaY0JqX2UxeWlPM29yLV9qTVhyMyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjYS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDMwMjEyNTk5MDM1OTgxMjM1MzUiLCJhdWQiOlsiY2FzdGluZyBhZ2VuY3kiLCJodHRwczovL2ZzbmRjYS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTg2MjI4MjM5LCJleHAiOjE1ODYyMzU0MzksImF6cCI6IllBWlhncWpoQ0NPQ3c1RUlnNHhsUWVYdWtlTktrQm1yIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.4vqV6F51qqsWAyWmo3fPV6ND3lXV59ofNkLEZUNHlMwZIALkittPf_eNf2zeIeDEMm0nzyCLr76gkhAWX5A4BMKfej3ITqea3fdJhlsXZk4kxac_puDKLQB76Qd0ztKekssT5Bt6J8zAvlYVhynGzeJU1ZUkWlyQKlRK93hPYd1-kePe5aMlRNQASZzJbXW_4iqICbYizFoupn01uryy4-fIO-GYyj5pxP20c9N26uA4B0VNQumZL85pVLP_Vx5CKGZTmu2Sylja9GrpA1OowN2OpnouMjjA3mEvn3woHkLtbDqBLK9EPA3xtLdFtoYHqeJIgm-ojbkASFegWlsA1Q'
        }

        self.casting_director_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZaY0JqX2UxeWlPM29yLV9qTVhyMyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjYS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDMyMzU5MTE1NDgzMjg3NjU2MTIiLCJhdWQiOlsiY2FzdGluZyBhZ2VuY3kiLCJodHRwczovL2ZzbmRjYS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTg2MjI4MzM4LCJleHAiOjE1ODYyMzU1MzgsImF6cCI6IllBWlhncWpoQ0NPQ3c1RUlnNHhsUWVYdWtlTktrQm1yIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.Q-vrzEMc9VTx0qGVR1yDAKTbqCSYuwD0y0xlsFgs2kGsEJKCn6u4MzYq5teq2LnkrL0iZqYhvDis8aXrD5kR8jCfBt_e5gJ2l1Jd9NUIcGmaWVDloIEOlavigTfqmQh2Wnk0JigyYe-O5UHWqwE1PCaNubdq81rYW4FisZrjDo59BmsE67oQl4QzUSy-a4EwHT63IBtF_1msdv_fHMuemJG6b57Mo9N0Oy8W0AzbdIAOzgrZV2rnI1tAWokR4mMCuXFXx4gdL-9R_iy8-F2YIiJ48nNkOYH-Vp-yXFvQSpYStlAQvxT-R85i-pFPKDS-l0Qn5bbe3ufR8oGmNkcYkA'
        }

        self.executive_producer_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZaY0JqX2UxeWlPM29yLV9qTVhyMyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjYS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTI2OTIyODc1OTYxOTA3NTA0MDMiLCJhdWQiOlsiY2FzdGluZyBhZ2VuY3kiLCJodHRwczovL2ZzbmRjYS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTg2MjI4MjgwLCJleHAiOjE1ODYyMzU0ODAsImF6cCI6IllBWlhncWpoQ0NPQ3c1RUlnNHhsUWVYdWtlTktrQm1yIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.ooZEJihSC4N-H8uoqimqeMm0tNUoybRL9kAuXymN0I9ujmn4Tkye0pbevz6XvAxb2s-UxWDysUPAHmd5F4av-azjGcZ3lat2BB3zM1ojvGEPtoXpGmSNmKML-ZEGM_hRGWT8GCnBbDDZffVDELttcbKQoU5PdFAneglPj-t2r6rHJ10IqdAllvyBEJziCNeYrQ_6lREhqkmTepGjIayBhN3wuQHbS56hfvwchg_NGqr0DqTJS5BkwKQa3u-LS9jm3PLh2SFogziH8litWAGlFqxzTel4NEBGUgOxEpqrv82whm1_uswvvId0zp7FryvIqmNGhkvlaiSu9yX8p3HhOw'
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
