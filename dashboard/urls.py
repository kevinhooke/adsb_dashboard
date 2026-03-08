from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("planesByDate/", views.heard_on_date, name="planesByDate"),
    path("today/", views.heard_today, name="today"),
]