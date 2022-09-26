from django.urls import path
from . import views

urlpatterns = [
    path('user_dashboard/',views.user_dashboard,name='user_dashboard'),
    path('user_login/',views.user_login,name='user_login'),
    path('user_logout/',views.user_logout,name='user_logout'),

    path('user_create_ticket/',views.user_create_ticket,name='user_create_ticket'),
    path('user_ticket_lists/',views.user_ticket_lists,name='user_ticket_lists'),
    path('user_delete_ticket/<int:id>',views.user_delete_ticket,name='user_delete_ticket'),
    
]