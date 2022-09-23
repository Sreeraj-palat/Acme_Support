from django.urls import path
from . import views

urlpatterns = [
    path('user_dashboard/',views.user_dashboard,name='user_dashboard'),
    path('user_login/',views.user_login,name='user_login'),
    path('user_logout/',views.user_logout,name='user_logout'),
]