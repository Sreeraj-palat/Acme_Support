from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from master.models import Department, Ticket
from .forms import create_user_form, create_department_form, CreateTicket
from accounts.decarators import allowed_users
from django.http import HttpRequest, HttpResponse
import datetime
from master.zenpy import zenpy_client
import zenpy

from zenpy.lib.api_objects import Ticket, User,CustomField



# Create your views here.

def home(request):
    return render(request,'welcome.html')

#Admin Dashboard view
@login_required(login_url = 'master_login')
def master_dashboard(request):
    if request.user.is_superadmin:
        users = Account.objects.all()
        user_count = users.count()
        department = Department.objects.all()
        department_count = department.count()
        
        context = {
            'user_count' : user_count,
            'department_count' : department_count,
            
            
        }
        return render(request, 'master/master_dashboard.html', context)
    else:
        return HttpResponse('Sorry You are not authorised to Access this page')    




#Admin Login
def master_login(request):
    if request.user.is_authenticated:
        return redirect('master')
    if request.method == 'POST':
        field = request.POST.get('field')
        password = request.POST.get('password')
        user = auth.authenticate(email=field,password=password)
        
        if not user:
            try:
                users = Account.objects.get(phone_number = field)
                print("User:",users)
                user = auth.authenticate(email = users.email ,password=password)
                print(user)
            except:
                messages.error(request,"credential wrong")
        if user is not None:
            auth.login(request,user)
            return redirect('master')
        else:
            messages.error(request,"credential wrong")
    return render(request,'master/master_login.html') 



#Admin Logout
@login_required(login_url = 'master_login')
def master_logout(request):
    if request.user.is_superadmin:
        auth.logout(request)
        messages.success(request, 'You are logged out.')
        return redirect('master_login')   
    else:
        return HttpResponse('Sorry You are not authorised to Access this page')    
     



#Create User view
@login_required(login_url = 'master_login')
def create_user(request):
    if request.user.is_superadmin:
        if request.method == 'POST':
            form = create_user_form(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                phone_number = form.cleaned_data['phone_number']
                email = form.cleaned_data['email']
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                department = form.cleaned_data['department']
                role = form.cleaned_data['role']
                

                user = Account.objects.create_user(
                    name = name,
                    username = username,
                    phone_number = phone_number,
                    email = email,
                    password = password,
                    

                )
                user.role = role
                user.department = department
                
                request.session['phone_number'] = phone_number
                print(phone_number)
                user.save()
                
                messages.success(request,'user created successfull')
                return redirect('users_list')            
                
        else:
            form = create_user_form()

        context = {
            'form' : form,
        }
        return render(request,'master/create_user.html', context)
    else:
        return HttpResponse('Sorry You are not authorised to Access this page')    



#Users List
@login_required(login_url = 'master_login')
def users_list(request):
    if request.user.is_superadmin:
        users = Account.objects.all()
        context = {
            'users':users,
        }
        return render(request,'master/user_list.html', context)

    else:
        return HttpResponse('Sorry You are not authorised to Access this page')    



#Create Department view
@login_required(login_url = 'master_login')
def creat_department(request):
    if request.user.is_superadmin:

        user = request.user
        form = create_department_form()
        if request.method == 'POST':
            form = create_department_form(request.POST, request.FILES)
            if form.is_valid():
                department = form.save(commit=False)
                department.Created_by = user
                department.save()
                return redirect('department_list')
            else:
                messages.warning(request, 'enter the correct details')

        context = {
            'form' : form,
            }        
        return render(request, 'master/create_department.html', context)
    else:
        return HttpResponse('Sorry You are not authorised to Access this page')    







#department list
@login_required(login_url = 'master_login')
def department_list(request):
    if request.user.is_superadmin:
        department = Department.objects.all()
        context = {
            'department':department,
        }
        return render(request,'master/department_list.html', context)
    else:
        return HttpResponse('Sorry You are not authorised to Access this page')    








#update Department View
@login_required(login_url = 'master_login')
def update_department(request,id):
    if request.user.is_superadmin:
        department = Department.objects.get(id=id)
        form = create_department_form(instance=department)
        if request.method == 'POST':
            form = create_department_form(request.POST, request.FILES, instance=department)
            if form.is_valid():
                form.save()
                return redirect('department_list')

        context = {
            'form' : form,
            'department' : department,
        }        
        return render(request, 'master/update_department.html', context)
    else:
        return HttpResponse('Sorry You are not authorised to Access this page')    



#delete Department view 
@login_required(login_url = 'master_login')
def delete_department(request,id):
    if request.user.is_superadmin:
        department = Department.objects.filter(id=id)
        print(department)    
        department_users = Account.objects.filter(department_id=id).exists()
        print(department_users)
        if department_users:
            messages.error(request, "you cant delete the department")
            return redirect('department_list')
        else :
            department.delete()  
        return redirect('department_list')
    else:
        return HttpResponse('Sorry You are not authorised to Access this page')   


#Create Ticket view
def create_ticket(request):
    user = Account.objects.filter(email= request.user).values('email','phone_number')
    form = CreateTicket(request.POST, user[0])
    print(request.user.email)
    if request.method == "POST":
        if form.is_valid():
            print('valid')
            Email = form.cleaned_data['email']
            Phone = form.cleaned_data['phone_number']
            Description = form.cleaned_data['description']
            Subject = form.cleaned_data['subject']
            Priority = form.cleaned_data['priority']
            zenpy_client.tickets.create(
            Ticket(description=Description,subject=Subject,priority=Priority,
                requester=User(name=request.user.name, email=request.user.email))
                )
            return redirect('ticket_lists')    
    context = {
        'form' : form,
    }        
    return render(request,'master/add_ticket.html', context)



#ticket list
def ticket_lists(request):
    tickets=[]
    for ticket in zenpy_client.search(type='ticket', assignee='sreerajpaalat@gmail.com'):
        tickets.append(ticket.to_dict())
       
        print(ticket)  
    context = {
        'tickets':tickets,
    }
    return render(request,'master/ticket_list.html', context)



#delete ticket
def delete_ticket(request,id):
    for ticket in zenpy_client.search(type='ticket', assignee='sreerajpaalat@gmail.com'):
        
        if ticket.id ==id:          
            zenpy_client.tickets.delete(ticket)
    return redirect('ticket_lists')



