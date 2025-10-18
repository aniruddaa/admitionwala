from django.test import TestCase, Client
from django.urls import reverse
from core.models import Job, JobInCareer, JobApplication


class JobApplyTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.job = Job.objects.create(title='Engineer', company='Acme')
        self.jinc = JobInCareer.objects.create(title='Informational Role', job_description='Info job')

    def test_get_apply_for_job(self):
        url = reverse('job_apply', args=[self.job.id])
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Apply for:')

    def test_get_apply_for_jobincareer(self):
        url = reverse('job_apply', args=[self.jinc.id])
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'This listing is informational')

    def test_post_creates_application_for_job(self):
        url = reverse('job_apply', args=[self.job.id])
        with open(__file__, 'rb') as f:
            r = self.client.post(url, {'name': 'Alice', 'email': 'a@example.com', 'phone': '123', 'education': 'BSc', 'resume': f})
        self.assertEqual(r.status_code, 302)  # redirect
        self.assertEqual(JobApplication.objects.filter(job=self.job).count(), 1)

    def test_post_creates_mapped_job_for_jobincareer(self):
        url = reverse('job_apply', args=[self.jinc.id])
        with open(__file__, 'rb') as f:
            r = self.client.post(url, {'name': 'Bob', 'email': 'b@example.com', 'phone': '456', 'education': 'MSc', 'resume': f})
        # should redirect
        self.assertEqual(r.status_code, 302)
        # find the created JobApplication
        app = JobApplication.objects.first()
        self.assertIsNotNone(app)
        # the job.company should start with JobInCareer:
        self.assertTrue(str(app.job.company).startswith('JobInCareer:'))
