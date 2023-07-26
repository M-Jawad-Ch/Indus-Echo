from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.index, name='main'),
    re_path(r".*favicon.ico.*", views.return_404),
    re_path(r"post/(?P<slug>.*)", views.get_post),
    re_path(r"(?P<slug>^(?!sitemap.xml).*)", views.get_category),
    re_path(r"(?P<category>.*)/(?P<post>.*)", views.get_post_via_category),
]
