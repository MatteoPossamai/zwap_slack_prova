from django.urls import path
from . import views

urlpatterns = [
    path('slack/events', views.Events.as_view(), name='event_hook'),
    path('top_zwappers/', views.TopZwappers.as_view(), name='top_zwappers'),
    path('postmark_template_email/', views.PostmarkTemplateEmail.as_view(), name='postmark_template_email'),
    path('postmark_plain_email/', views.PostmarkPlainTextEmail.as_view(), name='postmark_plain_email'),
    path('query_users/', views.QueryUsers.as_view(), name='query_users'),
]


"""
http://53a0-2001-b07-a5b-662a-a982-d45f-a305-1b48.ngrok.io/action/slack/events

/top_zwappers
http://53a0-2001-b07-a5b-662a-a982-d45f-a305-1b48.ngrok.io/action/top_zwappers/

/postmark_template_email
http://5982-2001-b07-a5b-662a-a982-d45f-a305-1b48.ngrok.io/action/postmark_template_email/

/postmark_plain_email
http://5982-2001-b07-a5b-662a-a982-d45f-a305-1b48.ngrok.io/action/postmark_plain_email/

/query_users
http://5982-2001-b07-a5b-662a-a982-d45f-a305-1b48.ngrok.io/action/query_users/
"""