from django.test import TestCase, Client
from django.contrib.auth.models import User
from core.models import Job, Bookmark

class BookmarkTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='bob', email='bob@example.com', password='pass')
        self.job = Job.objects.create(title='Test Job', company='Acme')

    def test_toggle_bookmark_requires_login(self):
        resp = self.client.post(f'/job/{self.job.id}/bookmark/')
        self.assertEqual(resp.status_code, 302)  # login redirect

    def test_toggle_bookmark(self):
        self.client.login(username='bob', password='pass')
        resp = self.client.post(f'/job/{self.job.id}/bookmark/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data.get('ok'))
        self.assertTrue(data.get('saved'))
        self.assertTrue(Bookmark.objects.filter(user=self.user, job=self.job).exists())
        # toggle off
        resp2 = self.client.post(f'/job/{self.job.id}/bookmark/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(resp2.status_code, 200)
        data2 = resp2.json()
        self.assertTrue(data2.get('ok'))
        self.assertFalse(data2.get('saved'))
        self.assertFalse(Bookmark.objects.filter(user=self.user, job=self.job).exists())
