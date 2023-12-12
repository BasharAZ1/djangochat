from django.contrib import admin
from django.urls import path,include
from .import views
urlpatterns = [
    path('user/<str:username>/', views.index, name='index'),
    path('chat/<slug:slug>/', views.chatroom, name='chatroom'),
    path('create_privateroom',views.create_privateroom),
    path('deleteRoom/<slug:slug>/',views.delete_chatroom),
    path('test',views.test)
]
