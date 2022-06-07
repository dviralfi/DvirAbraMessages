"""
DvirAbraMessages Project URL Configuration

The `urlpatterns` list routes URLs to views.

"""

from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls')),
]

# Adding api-login page to the urlpatterns for users to log in.
# Using the rest_framework package that provide it. 
urlpatterns += [
    path('api-auth/', include("rest_framework.urls"))
]