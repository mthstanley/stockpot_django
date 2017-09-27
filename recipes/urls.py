from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^create/', views.create_recipe, name='create_recipe'),
    url(r'^show/(?P<recipe_id>[0-9]+)/$', views.show_recipe, name='show_recipe'),
]
