from rest_framework import serializers
from .models import College, Course, Review, CounselingRequest, News, CounselingSession

class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class CounselingRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounselingRequest
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = __import__('core.models', fromlist=['Job']).Job
        fields = ['id','title','company','location','description','apply_link','posted_at','is_remote']

# Serializer for CounselingSession
class CounselingSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CounselingSession
        fields = '__all__'
