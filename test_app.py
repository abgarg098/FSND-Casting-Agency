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
        self.database_path = "postgres://postgres:stemed@{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.casting_assistant_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZaY0JqX2UxeWlPM29yLV9qTVhyMyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjYS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTI2OTIyODc1OTYxOTA3NTA0MDMiLCJhdWQiOlsiY2FzdGluZyBhZ2VuY3kiLCJodHRwczovL2ZzbmRjYS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTg2MTc2MjkxLCJleHAiOjE1ODYxODM0OTEsImF6cCI6IllBWlhncWpoQ0NPQ3c1RUlnNHhsUWVYdWtlTktrQm1yIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.N3jJQbVa8AdL48CpR1k8EeT802tFuv2GU3crrz_Bblkw_WzqNSbLTT9VNAovxmJWsnjnUzQ_EFuC-5eHoXEvOGfifOdDiSiW_sVQ-6QYizyV_sdHOq2jPBC99FaHS86sv2hrhlOEC6_gitVywVr2j24Z3NlryX9l3SeMsoBIrzwkjd2ocaqqajQhzXfMWaEPdAZmfeCqAVKWK1e2MMXn3nytfeiFs1eUw6DfoNvk9tSZN0lovvUJThpXH6bPHG2991wlhKHWUJcFfFaLqLY6xNoBbycdjcYstQ4hqaHP2RgtZJE721O8B9ZFBH-FfqpoTQIMnyJwxew9SCV79Kv0ag'
        }

        self.casting_director_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZaY0JqX2UxeWlPM29yLV9qTVhyMyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjYS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDMyMzU5MTE1NDgzMjg3NjU2MTIiLCJhdWQiOlsiY2FzdGluZyBhZ2VuY3kiLCJodHRwczovL2ZzbmRjYS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTg2MTc2MzY3LCJleHAiOjE1ODYxODM1NjcsImF6cCI6IllBWlhncWpoQ0NPQ3c1RUlnNHhsUWVYdWtlTktrQm1yIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.RrlhoNpKiyQr7wOCjKWwxMdhQ8z5Wd2GfACvFEFdKMxEVegVcjVCq4MImVHsPT4PZyQh1ThX-WD0DmBCm1VA_ZBP_fyQM92qTKCVTQlQKtdfaw9QND2EodRT3WqxvBk-GIplqt0fBIeih0xVHL_bTAt2p9E7-gpBKYSqIs66hsxXHM_42LHZ_7oTyhcwCrsAzIijAfFoCztvvAsVswb1NYtWvvKdeSYeOHFM9Ao5Edji2XrI4hlq0rHrJalIKeC33ibFvWPhHoKkDLkLxtpJ8aU9EPu2PHbYjpX4VKA4OuDohlr3M3kf6nAMJshuILq5rG_rHVe7c4KK3Ljoh6YRwQ'
        }

        self.executive_producer_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZaY0JqX2UxeWlPM29yLV9qTVhyMyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjYS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDMwMjEyNTk5MDM1OTgxMjM1MzUiLCJhdWQiOlsiY2FzdGluZyBhZ2VuY3kiLCJodHRwczovL2ZzbmRjYS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTg2MTc2NDU0LCJleHAiOjE1ODYxODM2NTQsImF6cCI6IllBWlhncWpoQ0NPQ3c1RUlnNHhsUWVYdWtlTktrQm1yIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.W-NxA4vj37MVzsT7KR7xCvbrsMkx_zp-XJPdCgcJyt2EWDWXkZxSfIS0TQNtFebO-HBwomN-8LKk7-Z8z0hHJ4vNxSTvqih2h5S5QypASaHYsTbFkkL0tjMNHpMTmPbG_vQohak2w2RjqdO_GfwWjKhvBCw-DaPhQlwO4vuBjWaQxMhIIqot8c0P5OIrS9ze2B66QV6rTbe2ziU1VGgGyf1DRFuA24MPQjk27oA6gt-vBn4fR6KwTXkYtsPzyBHnpxZtL82WFvq9Pcr277BHehsfOv20nj35XFxmfgiD6M-mD9BzzywRvAXAVnVZmhnuSVi6uPuTGZ0FdKGx2eqhXA'
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
            '/actors/1', json={'age': "43"}, headers=self.casting_assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_patch_actors_casting_director(self):
        res = self.client().patch(
            '/actors/1', json={'age': "43"}, headers=self.casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actors_executive_producer(self):
        res = self.client().patch(
            '/actors/1', json={'age': "43"}, headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actors_does_not_exist(self):
        res = self.client().patch(
            '/actors/1000', json={'age': "43"}, headers=self.executive_producer_header)

        self.assertEqual(res.status_code, 404)

    def test_patch_actors_no_data(self):
        res = self.client().patch('/actors/1', headers=self.executive_producer_header)

        self.assertEqual(res.status_code, 422)

    # Test PATCH Movie
    def test_patch_movies_public(self):
        res = self.client().patch('/movies/1', json={'title': "Updated Title"})

        self.assertEqual(res.status_code, 401)

    def test_patch_movies_casting_assistant(self):
        res = self.client().patch('/movies/1',
                                  json={'title': "Updated Title"}, headers=self.casting_assistant_header)

        self.assertEqual(res.status_code, 401)

    def test_patch_movies_casting_director(self):
        res = self.client().patch('/movies/1',
                                  json={'title': "Updated Title"}, headers=self.casting_director_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movies_executive_producer(self):
        res = self.client().patch('/movies/1',
                                  json={'title': "Updated Title"}, headers=self.executive_producer_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movies_does_not_exist(self):
        res = self.client().patch('/movies/1000',
                                  json={'title': "Updated Title"}, headers=self.executive_producer_header)

        self.assertEqual(res.status_code, 404)

    def test_patch_movies_no_data(self):
        res = self.client().patch('/movies/1', headers=self.executive_producer_header)

        self.assertEqual(res.status_code, 422)

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
