from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import UserSerializer,RecruiterSerializer,JobPostSerializer,SkillsSerializer
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login as auth_login
from django.http import JsonResponse
from rest_framework import status
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
            user = User(email=recruiter['email'], password=make_password(recruiter['password']), is_active=True)
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
    


class RecruiterProfileUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        try:
            # Get the recruiter associated with the authenticated user
            recruiter = Recruiter.objects.get(user=request.user)
            
            # Extract data from the request
            data = request.data

            # Update recruiter fields
            recruiter.full_name = data.get('full_name', recruiter.full_name)
            recruiter.company_name = data.get('company_name', recruiter.company_name)
            recruiter.contact_number = data.get('contact_number', recruiter.contact_number)
            recruiter.address = data.get('address', recruiter.address)
            
            # Save updated recruiter information
            recruiter.save()

            # Return updated recruiter information
            updated_recruiter_data = {
                "full_name": recruiter.full_name,
                "company_name": recruiter.company_name,
                "contact_number": recruiter.contact_number,
                "address": recruiter.address,
                "created_at": recruiter.created_at,
                "updated_at": recruiter.updated_at,
            }

            return JsonResponse(updated_recruiter_data, status=status.HTTP_200_OK)
        
        except Recruiter.DoesNotExist:
            return JsonResponse({"error": "Recruiter profile not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

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
            skills = data.get('skills', None)

            if not skills:
                return JsonResponse({"error": "Skills are required"}, status=400)
            
            job_post_serializer = JobPostSerializer(data=data)
            if job_post_serializer.is_valid():
                job_post = job_post_serializer.save(recruiter_id=recruiter)
                
                
                job_post.skills.set(skills) 
                response_data = {
                    "status": "Job post created successfully!",
                    "job_post": {
                        "title": job_post.title,
                        "description": job_post.description,
                        "location": job_post.location,
                        "salary_range": job_post.salary_range,
                        "experience_required": job_post.experience_required,
                        "skills": SkillsSerializer(job_post.skills.all(), many=True).data
                    }
                }
                return JsonResponse(response_data, status=201)
            else:
                return JsonResponse(job_post_serializer.errors, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        

class JobPostUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, job_post_id):
        try:
            # Fetch the job post ensuring it belongs to the authenticated user
            job_post = JobPost.objects.get(id=job_post_id, recruiter_id__user=request.user)
            
            # Get the updated data from the request
            data = request.data
            skills = data.pop('skills', None)  # Get skills if provided

            # Initialize the serializer with the job post instance and data
            job_post_serializer = JobPostSerializer(job_post, data=data, partial=True)
            
            if job_post_serializer.is_valid():
                # Save the updated job post
                job_post = job_post_serializer.save()

                # Update skills if provided
                if skills is not None:
                    job_post.skills.set(skills)

                # Return the updated job post details
                return JsonResponse(job_post_serializer.data, status=status.HTTP_200_OK)
            else:
                return JsonResponse(job_post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except JobPost.DoesNotExist:
            return JsonResponse({"error": "Job post not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class JobPostList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        try:
            # Retrieve the recruiter associated with the authenticated user
            recruiter = Recruiter.objects.get(user=request.user)

            # Filter job posts based on the recruiter
            job_posts = JobPost.objects.filter(recruiter_id=recruiter)

            # Serialize the job posts
            response_data = []
            for job_post in job_posts:
                skills = job_post.skills.all()
                skills_list = [skill.title for skill in skills]
                
                job_post_data = {
                    "id": job_post.id,
                    "title": job_post.title,
                    "description": job_post.description,
                    "location": job_post.location,
                    "salary_range": job_post.salary_range,
                    "experience_required": job_post.experience_required,
                    "skills": skills_list,
                    "created_at": job_post.created_at,
                    "updated_at": job_post.updated_at
                }
                
                response_data.append(job_post_data)

            return JsonResponse(response_data, safe=False, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)