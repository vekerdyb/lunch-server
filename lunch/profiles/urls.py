from django.conf.urls import url
from lunch.profiles.views import MeView, OptionByUUID

urlpatterns = [
    url(r'^', MeView.as_view(), name='profile-me'),
    url(r'^(?P<uuid>)/option/', OptionByUUID.as_view(), name='profile-option'),
]
