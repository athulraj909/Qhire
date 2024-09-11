from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']


class RecruiterSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    class Meta:
        model = Recruiter
        fields = ['user','full_name','company_name','contact_number','address','created_at','updated_at']


class JobPostSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(many=True, queryset=Skills.objects.all())

    class Meta:
        model = JobPost
        fields = ['id', 'recruiter', 'title', 'description', 'location', 'salary_range', 'experience_required', 'skills', 'created_at', 'updated_at']
