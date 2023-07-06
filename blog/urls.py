from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='main'),
    path("post/<str:slug>/", views.get_post),
    path("<str:slug>/", views.get_category),
    path("<str:category>/<str:post>", views.get_post_via_category)
]
