from django.db import models  # type: ignore
from django.contrib.auth.models import User  # type: ignore

class CounselingSession(models.Model):
    name = models.CharField(max_length=100)
    interest = models.CharField(max_length=100)
    budget = models.IntegerField()
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} - {self.interest} - {self.location}"

class College(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='college_logos/', blank=True, null=True)
    background_image = models.ImageField(upload_to='college_backgrounds/', blank=True, null=True)
    phone = models.CharField(max_length=40, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    def __str__(self): return self.name

class Course(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=200)
    stream = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    eligibility = models.TextField(blank=True)
    fees = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True)
    brochure = models.FileField(upload_to='course_brochures/', blank=True, null=True)
    def __str__(self): return f"{self.name} ({self.college.name})"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    interested_streams = models.CharField(max_length=200, blank=True)
    def __str__(self): return self.user.username

class Review(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(default=5)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.college.name} - {self.rating}"

class CounselingRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')
    def __str__(self): return f"{self.name} ({self.status})"

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True)
    def __str__(self): return self.title


class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    apply_link = models.URLField(blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    is_remote = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.title} @ {self.company}"


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    education = models.CharField(max_length=255, blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Application: {self.name} -> {self.job.title}"

from django.db import models  # type: ignore

class CertifiedCourse(models.Model):
    title = models.CharField(max_length=255)
    ppt_file = models.FileField(upload_to='courses/ppt/')
    post_image = models.ImageField(upload_to='courses/images/')
    
    def __str__(self):
        return self.title


class JobInCareer(models.Model):
    title = models.CharField(max_length=255)
    job_description = models.TextField()
    job_image = models.ImageField(upload_to='jobs/images/')
    
    def __str__(self):
        return self.title


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user} saved {self.job}"


class AboutPage(models.Model):
    """Singleton-ish model to store about page content editable via admin."""
    title = models.CharField(max_length=200, default='About Us')
    subtitle = models.CharField(max_length=300, blank=True)
    content = models.TextField(blank=True)
    what_we_do = models.TextField(blank=True, help_text='Short HTML or markdown describing what we do')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "About Page"


class Director(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='about/directors/', blank=True, null=True)

    def __str__(self):
        return self.name


class StaffMember(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='about/staff/', blank=True, null=True)

    def __str__(self):
        return self.name
