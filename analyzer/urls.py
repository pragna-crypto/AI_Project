from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_speech, name='upload'),
    path('results/<int:pk>/', views.results, name='results'),
    path('history/', views.history, name='history'),
]
