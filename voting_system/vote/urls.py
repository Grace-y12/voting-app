from django.urls import path, include

from . import views
from django.conf import settings
from django.conf.urls.static import static
# vote/urls.py (or the appropriate app file)
from django.urls import path
from django.shortcuts import redirect
from django.contrib import admin
from . import views



urlpatterns = [
      
    path('', views.homepage, name='homepage'),
    path('login/', views.login_view , name='login'),
    path('register/', views.register_page, name='register'),
    path('regulations/', views.regulations, name='regulations'),
    path('voting/', views.voting_page, name='voting'),
    path('submit_vote/', views.submit_vote, name='submit_vote'),
    path('cast-vote/', views.cast_vote, name='cast_vote'),
    path('live-results/', views.live_results, name='live_results'),
    path('results/', views.results_view, name='results_page'),
    path('vote-counts/', views.get_vote_counts, name='vote_counts'),
    path('committee_register/', views.committee_register, name='committee_register'),
    


    
    ] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)