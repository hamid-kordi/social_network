from django.urls import path
from . import views

name = "home"
urlpatterns =[path("", views.HomeView.as_view(), name="home")] 
