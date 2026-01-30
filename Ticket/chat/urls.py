from django.urls import path
from . import views

urlpatterns = [
    path('api/send/', views.send_message, name='chat_send'),
    path('api/get/', views.get_messages, name='chat_get'),
]
