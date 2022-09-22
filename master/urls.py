from django.urls import path
from . import views

urlpatterns = [
    path('master/',views.master_dashboard,name='master'),
    
    

]