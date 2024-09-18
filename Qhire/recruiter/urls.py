from django.contrib import admin
from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework.routers import DefaultRouter
from recruiter.views import UserViewSet,RecruiterViewSet

router = DefaultRouter()
router.register('user', UserViewSet)
router.register('recruiter', RecruiterViewSet)

urlpatterns = [
    
    path('register/recruiter',RecruiterRegister.as_view(),name="recruiterregister"),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh', TokenRefreshView.as_view()),
    # path('token/', tokenLease.as_view()),
    path('profile/', RecruiterProfile.as_view(), name='profile'),
    path('profile/update/', RecruiterProfileUpdate.as_view(), name='profile-update'),
    path('logout/', LogoutView.as_view(), name='logout'),


    path('jobpost/create/', JobPostCreate.as_view(), name='jobpost_create'),
    path('jobpost/', JobPostList.as_view(), name='jobpost-list'),
    path('jobpost/update/<int:job_post_id>/', JobPostUpdate.as_view(), name='jobpost_update'),



]
