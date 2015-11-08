from django.conf.urls import url
from lunch.profiles.views import MeView, CardView

urlpatterns = [
    url(r'^(?P<pk>\d+)/card/', CardView.as_view(), name=CardView.URL_NAME),
    url(r'^$', MeView.as_view(), name='profile-me'),
]
