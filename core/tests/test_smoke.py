from django.test import TestCase, Client
from django.contrib.auth.models import User

# import models here for use inside test methods
from core.models import College, Course


class AuthSmokeTests(TestCase):
    def setUp(self):
        # create a test user
        self.email = 'smoketest@example.com'
        self.password = 'smoketestpass'
        User.objects.create_user(username=self.email, email=self.email, password=self.password)
        self.client = Client()

    def test_login_and_pages(self):
        # login
        login_ok = self.client.login(username=self.email, password=self.password)
        self.assertTrue(login_ok, 'Login failed for smoke test user')

        # profile page
        resp = self.client.get('/profile/')
        self.assertEqual(resp.status_code, 200)
        content = resp.content.decode('utf-8')
        # basic check: page should mention 'Your Profile' heading
        self.assertIn('Your Profile', content)

        # dashboard page
        resp2 = self.client.get('/dashboard/')
        self.assertEqual(resp2.status_code, 200)
        content2 = resp2.content.decode('utf-8')
        # dashboard should greet the user or show dashboard heading
        self.assertTrue('User Dashboard' in content2 or 'Welcome' in content2)

    def test_exams_and_careers_pages(self):
        # exams and careers pages should be accessible
        r = self.client.get('/exams/')
        self.assertEqual(r.status_code, 200)
        r2 = self.client.get('/careers/')
        self.assertEqual(r2.status_code, 200)

    def test_courses_list_and_detail(self):
        # create a sample college and course
        c = College.objects.create(name='Sample College', location='Mumbai')
        course = Course.objects.create(college=c, name='Sample Course', stream='Engineering', duration='4 years')

        rc = self.client.get('/courses/')
        self.assertEqual(rc.status_code, 200)
        rcd = self.client.get(f'/course/{course.id}/')
        self.assertEqual(rcd.status_code, 200)
