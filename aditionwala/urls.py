from django.contrib import admin
from django.urls import path, include
from core import views
from rest_framework import routers
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import StaticViewSitemap, CollegeSitemap
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'colleges', views.CollegeViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'counseling', views.CounselingRequestViewSet)
router.register(r'news', views.NewsViewSet)
router.register(r'jobs', views.JobViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('apply/', views.apply_one_form, name='apply_one_form'),
    path('profile/', views.profile, name='profile'),
    path('counseling/', views.counseling_form, name='counseling_form'),
    path('colleges/', views.college_list, name='college_list'),
    path('college/<int:college_id>/', views.college_detail, name='college_detail'),
    path('admition-counseling/', views.admition_counseling, name='admition_counseling'),
    path('exams/', views.exams, name='exams'),
    path('careers/', views.careers, name='careers'),
    path('job/<int:job_id>/', views.job_detail_view, name='job_detail'),
    path('job/<int:job_id>/apply/', views.job_apply_view, name='job_apply'),
    path('job/<int:job_id>/easy-apply/', views.job_easy_apply, name='job_easy_apply'),
    path('job/<int:job_id>/easy_apply/', views.easy_apply_view, name='job_easy_apply'),
    path('job/<int:job_id>/bookmark/', views.toggle_bookmark_view, name='job_bookmark'),
    path('job/<int:job_id>/recommendations/', views.job_recommendations, name='job_recommendations'),
    path('company/<str:company_name>/', views.company_detail, name='company_detail'),
    path('about/', views.about_page, name='about'),
    path('courses/', views.courses_list, name='courses_list'),
    path('course/<int:course_id>/', views.course_detail_view, name='course_detail'),
    path('api/health', views.api_health),
    path('api/predict', views.api_predict),
    path('api/recommend', views.api_recommend),
    path('api/colleges-autocomplete/', views.colleges_autocomplete, name='colleges_autocomplete'),
    path('api/', include(router.urls)),
    path('sitemap.xml', sitemap, {'sitemaps': {'static': StaticViewSitemap, 'colleges': CollegeSitemap}}, name='sitemap'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
