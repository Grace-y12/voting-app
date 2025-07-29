# urls.py

from django.contrib import admin
from django.urls import path, include
from vote import views  # Your views file
from django.shortcuts import redirect
from django.contrib import admin






urlpatterns = [
    
    
    path('admin/', admin.site.urls), 
    path('committee_login/', views.committee_login, name='committee_login'), # Default admin URL pattern
    path('', include('vote.urls')),  # Other routes for your app
]




    

