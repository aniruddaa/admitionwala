from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from core.models import College


class MetaTagsSmokeTests(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user('tester', 'tester@example.com', 'pass')
        # create a sample college
        self.college = College.objects.create(name='Test College', location='Test City')

    def test_pages_have_meta_and_render(self):
        # home
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'<meta name="description"', r.content)

        # colleges list
        r = self.client.get('/colleges/')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'<meta property="og:title"', r.content)

        # college detail
        r = self.client.get(f'/college/{self.college.id}/')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'CollegeOrUniversity', r.content)

        # profile (requires login)
        self.client.login(username='tester', password='pass')
        r = self.client.get('/profile/')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Profile', r.content)
