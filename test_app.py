import unittest
import json
from app import app

class CoffeeRecommendationTest(unittest.TestCase):
    
    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        # Test the home route
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Find Your Perfect Coffee', result.data)

    def test_valid_recommendation(self):
        # Test the recommendation route with valid input
        preferences = {
            'roast_level': 'Medium',
            'acidity': 'High',
            'drink_type': 'Espresso',
            'description': 'Fruity',
            'drink_time': 'Morning',
            'strength': 'Strong'
        }
        result = self.app.post('/recommend', data=json.dumps(preferences), content_type='application/json')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Country', result.data)

    def test_invalid_recommendation(self):
        # Test the recommendation route with invalid input
        preferences = {
            'roast_level': 'InvalidLevel',  # Invalid roast level
            'acidity': 'High',
            'drink_type': 'Espresso',
            'description': 'Fruity',
            'drink_time': 'Morning',
            'strength': 'Strong'
        }
        result = self.app.post('/recommend', data=json.dumps(preferences), content_type='application/json')
        self.assertEqual(result.status_code, 400)
        self.assertIn(b'Some of your inputs are not recognized', result.data)

if __name__ == '__main__':
    unittest.main()
