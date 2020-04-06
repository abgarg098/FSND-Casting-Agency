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
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZaY0JqX2UxeWlPM29yLV9qTVhyMyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjYS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMTI2OTIyODc1OTYxOTA3NTA0MDMiLCJhdWQiOlsiY2FzdGluZyBhZ2VuY3kiLCJodHRwczovL2ZzbmRjYS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTg2MTU5MjY0LCJleHAiOjE1ODYxNjY0NjQsImF6cCI6IllBWlhncWpoQ0NPQ3c1RUlnNHhsUWVYdWtlTktrQm1yIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.D5FlmJ2cnXyo5_d2H985XstMC96z3uUd9Z8rg-PA2YWMD21kpnpNgfDSW491MPhJQbKhiWHsv82eUxW10TPjBw9-vibVGbe6SvwX0lHvuQfDUy_plf_pTC6J9PXLcVPapbGhdysHvWZ7cSNJ7Z2Qw5rONcVTPC2-RwNFX-8xuqVTpbY_-Beb35WD2Q4OT100w1KhIoJYvLIXZ4u13wZPn9kFdS8yjxp89KNk8VvYbfUaCXTtfuD8ZEarQuNRZsCvfzei5tnbAGy4OPrqI6KI7KKT84CeYpr_l9ZxiWBz7SgUMe_NSmgWWD_wk4vBQT3GPlOxSiHhb_AdATEW8MmxMw'
        }

        self.casting_director_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZaY0JqX2UxeWlPM29yLV9qTVhyMyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjYS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDMyMzU5MTE1NDgzMjg3NjU2MTIiLCJhdWQiOlsiY2FzdGluZyBhZ2VuY3kiLCJodHRwczovL2ZzbmRjYS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTg2MTU5NDY4LCJleHAiOjE1ODYxNjY2NjgsImF6cCI6IllBWlhncWpoQ0NPQ3c1RUlnNHhsUWVYdWtlTktrQm1yIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.h5zYORo6Ooca2vFQIw3XfkbcBY3OAa-GASvKNVp7uUl73VLAml3wydlgvI7jgSWdy1UBC424jt37yhVnk6nW0A69OyM_s8RZou3jWQMn1igh2-lS5ntNGx9KKrtM9EKtX0ssuT0-Opxmz1_T2hRGfdSBaW-62CiCRGHc73xMHewDgwLgSBdFhUOw1c0TAbOaroMLj2_QOBdbH31E9XzZ1fuXTLq56PTqK0VGIW2T-AhGf1sSPuRk0hDEO6JiwvNPB_XoAj_tsmyi1ewbJhhgURRDZ4rtCIyEwpmDVll2HvuYUV7EGrily0sa0wxMyObE6YRwvFbpctmyFPq7EJdNyA'
        }

        self.executive_producer_header = {
            'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZaY0JqX2UxeWlPM29yLV9qTVhyMyJ9.eyJpc3MiOiJodHRwczovL2ZzbmRjYS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDMwMjEyNTk5MDM1OTgxMjM1MzUiLCJhdWQiOlsiY2FzdGluZyBhZ2VuY3kiLCJodHRwczovL2ZzbmRjYS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTg2MTU5MzgxLCJleHAiOjE1ODYxNjY1ODEsImF6cCI6IllBWlhncWpoQ0NPQ3c1RUlnNHhsUWVYdWtlTktrQm1yIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.p3Pv2vPl9eQ8vc5r4VJagRvruNkm0XV89biuKrwJp0upGg_O1cQaQUdiE20DFKuM28xpnss5SZFMkA6A4kUYwcm5yFyqQ-jHvx1yFvVi1wVh1Nl9Mquqje2Eh2tKLeVOVQQZCW4b-BRC1VbMSi8RC_ePL4_rp1hd5ogN3Q9dzsEkHz1TtJzoVsubBAjKrOKzCSVn7f1qamCaStkYtf-lTTp0wshQo6pLFvKe0e13KKYDA2qnr6So2oPbreEvOYW-zFz_9ojBOe1HxJjfNKMf0X9IzveYzmvC7Ke-N_zkdemUntQ8llJ2T-7YLRZHj6MT6-zTi1inRa_uEyvaEJA7Bg'
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
        
        self.assertEqual(res.status_code, 422)

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