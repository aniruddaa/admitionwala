from django.test import TestCase, Client
from core.models import College


class CollegesAutocompleteTests(TestCase):
    def setUp(self):
        College.objects.create(name='Alpha Institute', location='Mumbai')
        College.objects.create(name='Beta College', location='Bangalore')
        College.objects.create(name='Gamma University', location='Delhi')
        self.client = Client()

    def test_autocomplete_by_name(self):
        resp = self.client.get('/api/colleges-autocomplete/', {'q': 'Alpha'})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('results', data)
        self.assertTrue(any(r['name'] == 'Alpha Institute' for r in data['results']))

    def test_autocomplete_by_location(self):
        resp = self.client.get('/api/colleges-autocomplete/', {'q': 'Bangalore'})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(any('Bangalore' in r['location'] for r in data['results']))
