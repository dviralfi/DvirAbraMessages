from django.urls import path
from . import views

urlpatterns = [

    path('<str:username>/messages/', views.get_all_messages, name='get_all_messages'),
    
    path('<str:username>/messages/<int:id>/', views.message, name='message'),

    path('<str:username>/messages/write/', views.write_message, name='write_message'),

    path('<str:username>/messages/unread/', views.get_unread_messages, name='get_unread_messages'),
    
]
