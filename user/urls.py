from django.urls import path
from . import views

urlpatterns = [
    path('user_dashboard/',views.user_dashboard,name='user_dashboard'),
    path('user_login/',views.user_login,name='user_login'),
    path('user_logout/',views.user_logout,name='user_logout'),


    path('user_add_ticket/',views.user_add_ticket,name='user_add_ticket'),
    path('user_ticket_list/',views.user_ticket_list,name='user_ticket_list'),
    path('user_update_ticket/<int:id>',views.user_update_ticket,name='user_update_ticket'),
    path('user_delete_ticket/<int:id>',views.user_delete_ticket,name='user_delete_ticket'),
]