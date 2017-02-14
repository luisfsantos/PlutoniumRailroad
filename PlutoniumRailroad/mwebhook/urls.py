from django.conf.urls import url
from mwebhook import views
urlpatterns = [
    url(r'^$', views.webhook),
]
