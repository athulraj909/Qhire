from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import UserSerializer,RecruiterSerializer,JobPostSerializer
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login as auth_login
from django.http import JsonResponse
import json
import jwt
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken





User = get_user_model()



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RecruiterViewSet(viewsets.ModelViewSet):
    queryset = Recruiter.objects.all()
    serializer_class = RecruiterSerializer




class RecruiterRegister(APIView):
    def post(self,request,format=None):
        try:
            recruiter = request.data.get('recruiter')
            print(recruiter)
            data = request.data.get('data')
            print(data)
            user = User(username=recruiter['email'], email=recruiter['email'], password=make_password(recruiter['password']))
            user.save()
            recruiter_data = Recruiter.objects.create(
                user = user,
                full_name = data['full_name'],
                company_name = data['company_name'],
                contact_number = data['contact_number'],
                address = data['address'],
            )
            recruiter_data.save()
            print(f"Recruiter : {recruiter_data}")

            
            data1 = {"status" : 1}
            return JsonResponse(data1,safe=False)

        except Exception as e:
            print(e)
            data1 = {"status" : 0}
            return JsonResponse(data1,safe=False)
            



class RecruiterProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_data = {
            "email": user.email,
            "recruiter_info": {},
        }
        try:
            recruiter_info = Recruiter.objects.get(user_id=user)
            user_data["recruiter_info"] = {
                "full_name": recruiter_info.full_name,
                "company_name": recruiter_info.company_name,
                "contact_number": recruiter_info.contact_number,
                "address": recruiter_info.address,
                "created_at": recruiter_info.created_at,
                "updated_at": recruiter_info.updated_at,
                
            }
        except Recruiter.DoesNotExist:
            pass

        return JsonResponse(user_data)
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            # Extract the refresh token from the request
            refresh_token = request.data.get('refresh_token')
            
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return JsonResponse({'status': 'Successfully logged out'}, status=205)  # 205 Reset Content

            return JsonResponse({'error': 'Refresh token is required'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)




class JobPostCreate(APIView):
    def post(self, request):
        try:
            data = request.data
            recruiter = Recruiter.objects.get(user=request.user)
            skills = data.pop('skills', [])
            
            job_post_serializer = JobPostSerializer(data=data)
            if job_post_serializer.is_valid():
                job_post = job_post_serializer.save(recruiter=recruiter)
                
                # Add the many-to-many relationship with skills
                job_post.skills.set(skills)  # Assign the skills to the job post
                return JsonResponse({"status": "Job post created successfully!"}, status=201)
            else:
                return JsonResponse(job_post_serializer.errors, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)