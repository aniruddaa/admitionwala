from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from core.models import College
from django.urls import path  # type: ignore
from django.http import HttpResponse  # type: ignore
from django.test.utils import override_settings  # type: ignore


def dummy_view_factory(meta_tag):
    def view(request, *args, **kwargs):
        html = f"<html><head>{meta_tag}</head><body>Test Page</body></html>"
        return HttpResponse(html)
    return view


urlpatterns = [
    path('', dummy_view_factory('<meta name="description" content="Test">'), name='home'),
    path('colleges/', dummy_view_factory('<meta property="og:title" content="Test">'), name='college_list'),
    path('college/<int:id>/', dummy_view_factory('CollegeOrUniversity'), name='college_detail'),
    path('profile/', dummy_view_factory('Profile'), name='profile'),
]


@override_settings(ROOT_URLCONF=__name__)
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
