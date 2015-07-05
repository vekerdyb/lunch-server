from django.conf.urls import url
from lunch.profiles.views import MeView

urlpatterns = [
    url(r'^', MeView.as_view(), name='profile-me'),
]
