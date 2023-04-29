from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.registerUser, name='user-registration'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.user_logout, name='logout'),
]