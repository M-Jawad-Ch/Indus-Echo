from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='main'),
    path("post/<str:slug>/", views.get_post),
]
