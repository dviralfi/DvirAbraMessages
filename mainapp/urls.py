from django.urls import path
from . import views

urlpatterns = [

    path('<str:username>/messages/', views.get_all_messages, name='get_all_messages'), # accept GET request
    
    path('<str:username>/messages/<int:id>/', views.message, name='message'), # accept GET/DELETE requests

    path('<str:username>/messages/write/', views.write_message, name='write_message'),# accept POST request

    path('<str:username>/messages/unread/', views.get_unread_messages, name='get_unread_messages'), # accept GET request

    path('', views.create_user, name='create_user'), # accept POST request

]
