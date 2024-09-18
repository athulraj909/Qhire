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

class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = ['id', 'title']

class JobPostSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(queryset=Skills.objects.all(), many=True)  
    class Meta:
        model = JobPost
        fields = ['id', 'title', 'description', 'location', 'salary_range', 'experience_required', 'skills']
        read_only_fields = ['created_at', 'updated_at', 'recruiter_id']
