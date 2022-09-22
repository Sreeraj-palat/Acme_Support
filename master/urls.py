from django.urls import path
from . import views

urlpatterns = [
    path('master/',views.master_dashboard,name='master'),
    path('master_login/',views.master_login,name='master_login'),
    path('master_logout/',views.master_logout,name='master_logout'),    

]