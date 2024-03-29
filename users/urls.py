from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^register/', views.register, name='register'),
    url(r'^show/(?P<username>[\w.@+-]+)/', views.show_profile, name='show_profile'),
    url(r'^edit/(?P<username>[\w.@+-]+)/', views.edit_profile, name='edit_profile'),
]
