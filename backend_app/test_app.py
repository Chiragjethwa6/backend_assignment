import unittest
import json
from app import app, db, Songs

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Test the /api/songs endpoint (GET all songs)
    def test_get_all_songs(self):
        with app.app_context():
            response = self.app.get('/api/songs')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 'Success')
            self.assertIsInstance(data['data'], list)

    # Test the /api/songs/<string:title> endpoint (GET song by title)
    def test_get_song_by_title(self):
        with app.app_context():
            response = self.app.get('/api/songs/Again')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 'Success')
            self.assertEqual(data['data']['title'], 'Again')

    # Test the /api/songs/<string:title> endpoint with a non-existent title
    def test_get_song_by_nonexistent_title(self):
        with app.app_context():
            response = self.app.get('/api/songs/nonexistentSong')
            self.assertEqual(response.status_code, 404)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 'Failed')
            self.assertEqual(data['message'], 'Song not found')

    # Test the /api/songs/rate/<string:id> endpoint (PUT request for rating a song)
    def test_rate_song(self):
        with app.app_context():
            payload = json.dumps({"star_rating": 4})
            response = self.app.put(
                '/api/songs/rate/7nT4rMprxiA9H9HM3oZ1Kq',
                data=payload,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 'Success')
            self.assertEqual(data['message'], 'Song rated successfully')

    # Test the /api/songs/rate/<string:id> endpoint with an invalid rating
    def test_rate_song_invalid_rating(self):
        with app.app_context():
            payload = json.dumps({"star_rating": 6})  # Invalid rating, more than 5
            response = self.app.put(
                '/api/songs/rate/7nT4rMprxiA9H9HM3oZ1Kq',
                data=payload,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 'Failed')
            self.assertEqual(data['message'], 'Rating must be between 1 and 5')

    # Test the /api/songs/rate/<string:id> endpoint with a non-existent song
    def test_rate_nonexistent_song(self):
        with app.app_context():
            payload = json.dumps({"star_rating": 3})
            response = self.app.put(
                '/api/songs/rate/nonexistentid',
                data=payload,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 404)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 'Failed')
            self.assertEqual(data['message'], 'Song not found')


if __name__ == '__main__':
    unittest.main()
