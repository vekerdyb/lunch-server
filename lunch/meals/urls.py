from django.conf.urls import url
from lunch.meals.views import TodayMealByUUID

urlpatterns = [
    url(r'^(?P<uuid>\w+)/meal/', TodayMealByUUID.as_view(), name=TodayMealByUUID.URL_NAME),
]
