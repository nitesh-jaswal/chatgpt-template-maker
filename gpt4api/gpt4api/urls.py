from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat_view'),
    path('chat', views.chat_view, name='chat_view'),
]
