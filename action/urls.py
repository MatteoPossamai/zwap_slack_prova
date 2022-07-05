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
http://d46e-2001-b07-a5b-662a-3d2c-7c4e-74b2-3e2e.ngrok.io/action/slack/events

/top_zwappers
http://1c24-2001-b07-a5b-662a-a111-4046-2878-73ec.ngrok.io/action/top_zwappers/

/postmark_template_email
http://4d0b-2001-b07-a5b-662a-5147-53ed-8080-60b4.ngrok.io/action/postmark_template_email/

/postmark_plain_email
http://4d0b-2001-b07-a5b-662a-5147-53ed-8080-60b4.ngrok.io/action/postmark_plain_email/

/query_users
http://5b03-2001-b07-a5b-662a-a111-4046-2878-73ec.ngrok.io/action/query_users/

JRPC django
"""