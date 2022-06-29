from django.urls import include, path
from . import views

urlpatterns = [
    path('slack/events', views.Events.as_view(), name='event_hook'),
]

#http://ee32-2001-b07-a5b-662a-d8f8-a8c7-bee7-2d21.ngrok.io/action/slack/events