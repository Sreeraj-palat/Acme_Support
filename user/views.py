from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from master.forms import CreateTicket
import datetime

from master.zenpy import zenpy_client
import zenpy

from zenpy.lib.api_objects import Ticket, User,CustomField


# Create your views here.
@login_required(login_url = 'user_login')
def user_dashboard(request):
    return render(request,'user/user_dashboard.html')


#User Login
def user_login(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')
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
            return redirect('user_dashboard')
        else:
            messages.error(request,"credential wrong")
    return render(request,'user/user_login.html')     



#User Logout
@login_required(login_url = 'user_login')
def user_logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('user_login')    





# user Create Ticket view
def user_create_ticket(request):
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
    context = {
        'form' : form,
    }        
    return render(request,'user/user_add_ticket.html', context)



# user ticket list
def user_ticket_lists(request):
    tickets=[]
    for ticket in zenpy_client.search(type='ticket', assignee='sreerajpaalat@gmail.com'):
        tickets.append(ticket.to_dict())
       
        print(ticket)  
    context = {
        'tickets':tickets,
    }
    return render(request,'user/user_ticket_list.html', context)



# userdelete ticket
def user_delete_ticket(request,id):
    for ticket in zenpy_client.search(type='ticket', assignee='sreerajpaalat@gmail.com'):
        
        if ticket.id ==id:          
            zenpy_client.tickets.delete(ticket)
    return redirect('user_ticket_lists')

