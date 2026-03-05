from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("planesByDate/", views.heardOnDate, name="planesByDate"),
]