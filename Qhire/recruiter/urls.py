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
    path('logout/', LogoutView.as_view(), name='logout'),


]
