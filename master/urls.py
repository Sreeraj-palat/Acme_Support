from django.urls import path
from . import views

urlpatterns = [
    path('master/',views.master_dashboard,name='master'),
    path('master_login/',views.master_login,name='master_login'),
    path('master_logout/',views.master_logout,name='master_logout'),    

    path('create_user/',views.create_user,name='create_user'),
    path('users_list/',views.users_list,name='users_list'),


    path('create_department/',views.creat_department,name='create_department'),
    path('department_list/',views.department_list,name='department_list'),
    path('update_department/<int:id>',views.update_department,name='update_department'),
    path('delete_department/<int:id>',views.delete_department,name='delete_department'),


    path('add_ticket/',views.add_ticket,name='add_ticket'),
    path('ticket_list/',views.ticket_list,name='ticket_list'),
    path('update_ticket/<int:id>',views.update_ticket,name='update_ticket'),
    path('delete_ticket/<int:id>',views.delete_ticket,name='delete_ticket'),

]