"""
DvirAbraMessages Project URL Configuration

The `urlpatterns` list routes URLs to views.

"""

from django.contrib import admin
from django.urls import path,include
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls')),
]

# Adding a login page to the urlpatterns for users to log in.

urlpatterns += [
    path('login/', obtain_auth_token, name="obtain-auth-token"), # POST request to this url with the appropriate credentials, will return the Secret Auth TOKEN each user have.
]