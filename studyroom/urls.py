from django.urls import path
from . import views as v

urlpatterns = [
    path('login/',v.loginUser, name='login'),
    path('logout/',v.logoutUser, name='logout'),
    path('signup/',v.signupView,name='signup'),
    path('profile/<str:pk>/',v.userProfile,name='profile'),

    path('',v.homeView,name='home'),
    path('room/<str:pk>/', v.roomView, name='room'),

    path('create-room', v.create_room, name = 'create-room'),
    path('update-room/<str:pk>/', v.update_room, name = 'update-room'),
    path('delete-room/<str:pk>/', v.delete_room, name = 'delete-room'),
    path('edit-message/<str:pk>/',v.edit_message,name= 'edit-message'),
    path('delete-message/<str:pk>/', v.delete_message, name = 'delete-message'),
    
]