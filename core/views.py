def admition_counseling(request):
    from .models import CounselingSession, College
    from django.db.models import Count
    if request.method == 'POST':
        name = request.POST.get('name')
        interest = request.POST.get('interest')
        budget = request.POST.get('budget')
        location = request.POST.get('location')
        # Save session
        CounselingSession.objects.create(name=name, interest=interest, budget=budget, location=location)
        # Find best matching college(s) and summarize
        sessions = CounselingSession.objects.filter(interest__iexact=interest, location__iexact=location)
        colleges = College.objects.filter(location__icontains=location, courses__stream__icontains=interest).distinct()
        summary = ""
        if colleges.exists():
            college = colleges.annotate(num=Count('reviews')).order_by('-num').first()
            summary = f"Hello {name}, ok, I will guide you. Based on your interest in {interest} and your preferred location {location}, here is a top recommendation: {college.name}. "
            summary += f"About the college: {college.description} " if college.description else ""
            courses = college.courses.all()
            if courses:
                summary += "Available courses include: " + ", ".join([c.name for c in courses[:3]]) + ". "
            reviews = college.reviews.all()
            if reviews:
                avg_rating = sum([r.rating for r in reviews]) / len(reviews)
                summary += f"The average student rating is {avg_rating:.1f} out of 5. "
                summary += "Sample review: '" + reviews[0].text + "'. "
            summary += "If you want more details, please visit the college page. This concludes your personalized counseling session."
        else:
            summary = f"Hello {name}, ok, I will guide you. Sorry, I could not find a perfect match for your interest in {interest} at {location}. Please try a different location or interest."
        return render(request, 'admition_counseling.html', {
            'summary': summary,
            'name': name,
            'interest': interest,
            'budget': budget,
            'location': location,
            'completed': True
        })
    return render(request, 'admition_counseling.html')
# API endpoints
from django.http import JsonResponse
def api_health(request):
    return JsonResponse({'status':'ok'})

def api_predict(request):
    import json
    body = json.loads(request.body.decode('utf-8'))
    model = NakeMl()
    score = model.score_lead(body.get('interestLevel',5), body.get('budgetK',5), body.get('subscribed', False))
    return JsonResponse({'score': score, 'hot': score>=0.5})

def api_recommend(request):
    import json
    body = json.loads(request.body.decode('utf-8'))
    model = NakeMl()
    recs = model.recommend_services(body.get('interestLevel',5), body.get('budgetK',5), body.get('subscribed', False))
    return JsonResponse({'score': recs[0], 'recommendations': recs[1]})
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseBadRequest
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import random
from .nake_ml import NakeMl
from .models import Job, JobInCareer, Bookmark


def colleges_autocomplete(request):
    """Return JSON list of colleges matching query `q` (id, name, location, logo).
    Limit results to 10. Case-insensitive substring match on name or location.
    """
    from django.http import JsonResponse
    q = request.GET.get('q', '').strip()
    results = []
    if q:
        qs = College.objects.filter(name__icontains=q) | College.objects.filter(location__icontains=q)
        qs = qs.distinct()[:10]
        for c in qs:
            results.append({
                'id': c.id,
                'name': c.name,
                'location': c.location,
                'logo': c.logo.url if c.logo else None,
            })
    return JsonResponse({'results': results})

def home(request):
    return render(request, 'home.html')


def exams(request):
    return render(request, 'exams.html')


def careers(request):
    # Provide a job-portal-like careers page: list Job objects with search
    q = request.GET.get('q','').strip()
    jobs = list(Job.objects.all().order_by('-posted_at'))
    # include JobInCareer entries so admin can post job images and they show on the careers page
    jobs_in_career = list(JobInCareer.objects.all().order_by('-id'))
    # Normalize JobInCareer into objects with similar attributes the template expects
    for j in jobs_in_career:
        jobs.append(type('J', (), {
            'title': j.title,
            'company': '',
            'location': '',
            'is_remote': False,
            'posted_at': None,
            'description': j.job_description,
            'apply_link': '',
            'job_image': j.job_image,
            'id': getattr(j, 'id', None)
        })())
    # basic search filtering on the combined list
    if q:
        jobs = [item for item in jobs if q.lower() in (str(getattr(item, 'title','')) + str(getattr(item, 'company','')) + str(getattr(item, 'location',''))).lower()]
    return render(request, 'careers.html', {'jobs': jobs, 'q': q})
def job_detail_view(request, job_id):
    from django.shortcuts import get_object_or_404
    # Try to find a real Job first; if not found, fall back to JobInCareer entries
    is_career_entry = False
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        try:
            j = JobInCareer.objects.get(id=job_id)
            job = type('J', (), {
                'title': j.title,
                'company': '',
                'location': '',
                'is_remote': False,
                'posted_at': None,
                'description': getattr(j, 'job_description', ''),
                'apply_link': '',
                'job_image': getattr(j, 'job_image', None),
                'id': j.id,
            })()
            is_career_entry = True
        except JobInCareer.DoesNotExist:
            get_object_or_404(Job, id=job_id)

    # mark jobs created from JobInCareer mapping (company starts with 'JobInCareer:')
    is_auto_mapped = False
    if not is_career_entry:
        try:
            is_auto_mapped = bool(getattr(job, 'company', '') and str(job.company).startswith('JobInCareer:'))
        except Exception:
            is_auto_mapped = False

    # compute whether current user has bookmarked this job (avoid DB calls in template)
    is_bookmarked = False
    try:
        if request.user.is_authenticated and not is_career_entry:
            is_bookmarked = Bookmark.objects.filter(user=request.user, job_id=getattr(job, 'id', None)).exists()
    except Exception:
        is_bookmarked = False
    # extract simple responsibilities / skills from the description when possible
    responsibilities = []
    skills = []
    try:
        import re
        desc = str(getattr(job, 'description', '') or '')
        # look for Responsibilities: ... Skills: ... sections
        m_resp = re.search(r'Responsibilities:?(.*?)(?:\n\s*Skills:|$)', desc, re.I | re.S)
        if m_resp:
            resp_text = m_resp.group(1).strip()
            responsibilities = [s.strip(' \n\r\t-•') for s in re.split(r'[\n\r]+|\\s*-\\s*', resp_text) if s.strip()]
        m_sk = re.search(r'Skills:?(.*)', desc, re.I | re.S)
        if m_sk:
            skills_text = m_sk.group(1).strip()
            skills = [s.strip(' .,-') for s in re.split(r'[,\n\r]+', skills_text) if s.strip()]
    except Exception:
        responsibilities = []
        skills = []

    # company stats and link
    company_jobs_count = 0
    company_link = None
    try:
        from django.urls import reverse
        if getattr(job, 'company', None):
            company_jobs_count = Job.objects.filter(company=getattr(job, 'company')).count()
            company_link = reverse('company_detail', args=[getattr(job, 'company')])
    except Exception:
        company_jobs_count = 0
        company_link = None

    return render(request, 'job_detail.html', {
        'job': job,
        'is_career_entry': is_career_entry,
        'is_auto_mapped': is_auto_mapped,
        'is_bookmarked': is_bookmarked,
        'responsibilities': responsibilities,
        'skills': skills,
        'company_jobs_count': company_jobs_count,
        'company_link': company_link,
    })


def job_apply_view(request, job_id):
    """User-facing application form for a job. GET shows the form; POST submits it.
    Handles mapping JobInCareer entries to persistent Job records so applications are stored.
    """
    from django.shortcuts import get_object_or_404, redirect
    from django.http import JsonResponse
    from django.core.mail import mail_admins
    from .models import JobApplication

    is_career_entry = False
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        try:
            j = JobInCareer.objects.get(id=job_id)
            job = type('J', (), {
                'title': j.title,
                'company': '',
                'location': '',
                'is_remote': False,
                'posted_at': None,
                'description': getattr(j, 'job_description', ''),
                'apply_link': '',
                'job_image': getattr(j, 'job_image', None),
                'id': j.id,
            })()
            is_career_entry = True
        except JobInCareer.DoesNotExist:
            get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        education = request.POST.get('education')
        resume = request.FILES.get('resume')

        errors = []
        if not name:
            errors.append('Name is required.')
        if not email:
            errors.append('Email is required.')

        if resume:
            allowed = {
                'application/pdf',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            }
            max_size = 5 * 1024 * 1024
            content_type = getattr(resume, 'content_type', '')
            if content_type not in allowed:
                errors.append('Resume must be PDF, DOC or DOCX.')
            if resume.size > max_size:
                errors.append('Resume file size must be 5 MB or less.')

        if errors:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'ok': False, 'errors': errors}, status=400)
            return render(request, 'job_apply.html', {'job': job, 'errors': errors, 'is_career_entry': is_career_entry})

        # Determine the target Job (map JobInCareer to persistent Job if needed)
        if is_career_entry:
            marker = f'JobInCareer:{getattr(job, "id", "")}'
            mapped = Job.objects.filter(company=marker).first()
            if not mapped:
                mapped = Job.objects.create(
                    title=getattr(job, 'title', 'Job'),
                    company=marker,
                    location=getattr(job, 'location', ''),
                    description=getattr(job, 'description', '')[:2000],
                    apply_link=''
                )
            target_job = mapped
        else:
            target_job = job

        JobApplication.objects.create(
            job=target_job,
            name=name,
            email=email,
            phone=phone or '',
            education=education or '',
            resume=resume
        )

        try:
            subject = f'New job application for {target_job.title}'
            body = f'Name: {name}\nEmail: {email}\nPhone: {phone or ""}\nEducation: {education or ""}\nJob: {target_job.title} (id={target_job.id})\nURL: {request.build_absolute_uri()}'
            mail_admins(subject, body, fail_silently=True)
        except Exception:
            pass

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'ok': True, 'message': 'Application submitted. Thank you.'})
        return redirect('job_detail', job_id=job_id)

    return render(request, 'job_apply.html', {'job': job, 'is_career_entry': is_career_entry})


@login_required
def job_easy_apply(request, job_id):
    """AJAX endpoint for logged-in users to quickly apply via modal.
    Expects POST with name/email/phone/education and optional resume.
    Returns JSON {ok: bool, errors: [...], message: str}
    """
    from django.http import JsonResponse
    from django.core.mail import mail_admins

    # find job or jobincareer
    try:
        job = Job.objects.get(id=job_id)
        is_career_entry = False
    except Job.DoesNotExist:
        try:
            j = JobInCareer.objects.get(id=job_id)
            job = type('J', (), {
                'title': j.title,
                'id': j.id,
                'description': getattr(j, 'job_description', ''),
            })()
            is_career_entry = True
        except JobInCareer.DoesNotExist:
            return JsonResponse({'ok': False, 'errors': ['Job not found']}, status=404)

    name = request.POST.get('name') or request.user.get_full_name() or request.user.username
    email = request.POST.get('email') or request.user.email
    phone = request.POST.get('phone')
    education = request.POST.get('education')
    resume = request.FILES.get('resume')

    errors = []
    if not name: errors.append('Name is required.')
    if not email: errors.append('Email is required.')
    # resume checks
    if resume:
        allowed = {
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        }
        if getattr(resume, 'content_type', '') not in allowed:
            errors.append('Resume must be PDF, DOC or DOCX.')
        if resume.size > 5*1024*1024:
            errors.append('Resume must be 5 MB or less.')

    if errors:
        return JsonResponse({'ok': False, 'errors': errors}, status=400)

    # map JobInCareer to persistent Job if needed
    if is_career_entry:
        marker = f'JobInCareer:{getattr(job, "id", "")}'
        mapped = Job.objects.filter(company=marker).first()
        if not mapped:
            mapped = Job.objects.create(title=getattr(job, 'title', 'Job'), company=marker, description=getattr(job, 'description', '')[:2000], apply_link='')
        target_job = mapped
    else:
        target_job = job

    app = JobApplication.objects.create(job=target_job, name=name, email=email, phone=phone or '', education=education or '', resume=resume)

    try:
        subject = f'Quick apply: {target_job.title}'
        body = f'Name: {name}\nEmail: {email}\nJob: {target_job.title} (id={target_job.id})\nUser: {request.user.username}\nURL: {request.build_absolute_uri()}'
        mail_admins(subject, body, fail_silently=True)
    except Exception:
        pass

    return JsonResponse({'ok': True, 'message': 'Application submitted. Thank you.'})


@login_required
def easy_apply_view(request, job_id):
    """AJAX endpoint for logged-in users to Easy Apply from a modal.
    Expects POST with name/email/phone/education and optional resume file.
    Returns JSON.
    """
    from django.http import JsonResponse
    from django.core.mail import mail_admins

    # lookup job or JobInCareer as before
    is_career_entry = False
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        try:
            j = JobInCareer.objects.get(id=job_id)
            # lightweight
            job = type('J', (), {'title': j.title, 'id': j.id})()
            is_career_entry = True
        except JobInCareer.DoesNotExist:
            return JsonResponse({'ok': False, 'errors': ['Job not found']}, status=404)

    if request.method != 'POST':
        return JsonResponse({'ok': False, 'errors': ['POST required']}, status=400)

    name = request.POST.get('name') or request.user.get_full_name() or request.user.username
    email = request.POST.get('email') or request.user.email
    phone = request.POST.get('phone')
    education = request.POST.get('education')
    resume = request.FILES.get('resume')

    errors = []
    if not name:
        errors.append('Name is required.')
    if not email:
        errors.append('Email is required.')

    if resume:
        allowed = {'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}
        if getattr(resume, 'content_type', '') not in allowed:
            errors.append('Resume must be PDF/DOC/DOCX')
        if resume.size > 5*1024*1024:
            errors.append('Resume must be 5 MB or less')

    if errors:
        return JsonResponse({'ok': False, 'errors': errors}, status=400)

    # map JobInCareer to Job if needed
    if is_career_entry:
        marker = f'JobInCareer:{getattr(job, "id", "")}'
        mapped = Job.objects.filter(company=marker).first()
        if not mapped:
            mapped = Job.objects.create(title=getattr(job, 'title', 'Job'), company=marker, description='Auto-mapped')
        target_job = mapped
    else:
        target_job = job

    app = JobApplication.objects.create(job=target_job, name=name, email=email, phone=phone or '', education=education or '', resume=resume)

    try:
        mail_admins(f'Easy apply: {target_job.title}', f'User {request.user} applied: {name} <{email}>', fail_silently=True)
    except Exception:
        pass

    return JsonResponse({'ok': True, 'message': 'Application submitted. Thank you.'})


@login_required
def toggle_bookmark_view(request, job_id):
    from django.http import JsonResponse
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Job not found'}, status=404)
    bm, created = Bookmark.objects.get_or_create(user=request.user, job=job)
    if not created:
        bm.delete()
        return JsonResponse({'ok': True, 'saved': False})
    return JsonResponse({'ok': True, 'saved': True})


def job_recommendations(request, job_id):
    """Return simple recommendations based on title keyword overlap."""
    from django.http import JsonResponse
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return JsonResponse({'results': []})
    title_words = set(str(job.title).lower().split())
    candidates = Job.objects.exclude(id=job.id)[:200]
    scored = []
    for c in candidates:
        score = len(title_words.intersection(set(str(c.title).lower().split())))
        if score>0:
            scored.append((score, c))
    scored.sort(key=lambda x: -x[0])
    results = [{'id': c.id, 'title': c.title, 'company': c.company} for _, c in scored[:5]]
    return JsonResponse({'results': results})
    


def courses_list(request):
    qs = Course.objects.select_related('college').all()
    return render(request, 'courses.html', {'courses': qs})


def course_detail_view(request, course_id):
    from django.shortcuts import get_object_or_404
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'course_detail.html', {'course': course})

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pwd = request.POST.get('password')
        if not email or not pwd:
            return render(request, 'signup.html', {'error':'Provide email and password'})
        if User.objects.filter(username=email).exists():
            return render(request, 'signup.html', {'error':'This email is already registered. Please sign in or use another email.'})
        user = User.objects.create_user(username=email, email=email, password=pwd)
    login(request, user)
    return redirect('profile')
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pwd = request.POST.get('password')
        user = authenticate(request, username=email, password=pwd)
        if user:
            login(request, user)
            # respect 'next' param when present
            next_url = request.POST.get('next') or request.GET.get('next')
            return redirect(next_url) if next_url else redirect('profile')
        return render(request, 'login.html', {'error':'Invalid credentials'})
    return render(request, 'login.html')


 

def logout_view(request):
    logout(request)
    return redirect('home')


# College search/list view (public)
def college_list(request):
    q = request.GET.get('q','')
    colleges = College.objects.all()
    if q:
        colleges = colleges.filter(name__icontains=q) | colleges.filter(location__icontains=q)
    return render(request, 'college_list.html', {'colleges': colleges})

# College detail view (public)
def college_detail(request, college_id):
    from django.shortcuts import get_object_or_404
    college = get_object_or_404(College, id=college_id)
    page_background_url = None
    if college.background_image:
        page_background_url = request.build_absolute_uri(college.background_image.url)
    return render(request, 'college_detail.html', {'college': college, 'page_background_url': page_background_url})


def company_detail(request, company_name):
    """Show all jobs for a company name (string match)."""
    qs = Job.objects.filter(company=company_name).order_by('-posted_at')
    return render(request, 'company_detail.html', {'company_name': company_name, 'jobs': qs})


def about_page(request):
    from .models import AboutPage, Director, StaffMember
    about = AboutPage.objects.first()
    directors = Director.objects.all()
    staff = StaffMember.objects.all()
    return render(request, 'about.html', {'about': about, 'directors': directors, 'staff': staff, 'page_background_url': None})


def sitemap_xml(request):
    """Produce a simple sitemap XML containing home and college detail pages."""
    urls = []
    # home
    urls.append(request.build_absolute_uri('/'))
    # colleges
    for c in College.objects.all():
        urls.append(request.build_absolute_uri(f'/college/{c.id}/'))
    # build XML
    xml_parts = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        xml_parts.append('  <url>')
        xml_parts.append(f'    <loc>{u}</loc>')
        xml_parts.append('  </url>')
    xml_parts.append('</urlset>')
    return HttpResponse('\n'.join(xml_parts), content_type='application/xml')


def robots_txt(request):
    host = request.get_host()
    lines = [
        "User-agent: *",
        "Disallow:",
        f"Sitemap: {request.scheme}://{host}/sitemap.xml",
    ]
    return HttpResponse('\n'.join(lines), content_type='text/plain')

# User dashboard
@login_required
def dashboard(request):
    requests = CounselingRequest.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'user': request.user, 'counseling_requests': requests})

# Counseling request form
def counseling_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        if not name or not email or not phone:
            return render(request, 'counseling_form.html', {'error':'All fields required'})
        CounselingRequest.objects.create(user=request.user if request.user.is_authenticated else None, name=name, email=email, phone=phone, message=message)
        return redirect('dashboard')
    return render(request, 'counseling_form.html', {'user': request.user})



@login_required
def apply_one_form(request):
    # Make the one-form apply flow require login
    if request.method == 'POST':
        # demo: accept and show success
        return render(request, 'apply.html', {'success': True})
    return render(request, 'apply.html')


@login_required
def profile(request):
    # Ensure user has a UserProfile object
    from .models import UserProfile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

# DRF viewsets
from rest_framework import viewsets
from .models import College, Course, Review, CounselingRequest, News
from .models import Job
from .serializers import CollegeSerializer, CourseSerializer, ReviewSerializer, CounselingRequestSerializer, NewsSerializer

class CollegeViewSet(viewsets.ModelViewSet):
    queryset = College.objects.all()
    serializer_class = CollegeSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class CounselingRequestViewSet(viewsets.ModelViewSet):
    queryset = CounselingRequest.objects.all()
    serializer_class = CounselingRequestSerializer

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('-posted_at')
    from .serializers import JobSerializer
    serializer_class = JobSerializer
