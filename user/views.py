from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from accounts.models import Account
from master.forms import add_ticket_form
import datetime

from master.models import Ticket


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




#user ticket view
@login_required(login_url = 'user_login')
def user_add_ticket(request):
    user = request.user
    form = add_ticket_form()
    if request.method=='POST':
        form = add_ticket_form(request.POST,request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = user
            ticket.email = user.email
            ticket.phone_number = user.phone_number
            form.save()

            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            ticket_id = current_date + str(ticket.id)
            ticket.ticket_id = ticket_id
            form.save()
            return redirect('user_ticket_list')

        else:
            messages.error(request, "enter correct details")
            return redirect('user_add_ticket')
    context = {
            'form' : form,
        }
    return render(request,'user/user_add_ticket.html', context)




#user ticket list
@login_required(login_url = 'user_login')
def user_ticket_list(request):
    user = request.user
    ticket = Ticket.objects.filter(user=user)
    context = {
            'ticket' : ticket,
        }
    return render(request,'user/user_ticket_list.html', context)


#user update ticket view
@login_required(login_url = 'user_login')
def user_update_ticket(request,id):
    ticket = Ticket.objects.get(id=id)
    form = add_ticket_form(instance=ticket)
    if request.method == 'POST':
        form = add_ticket_form(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('user_ticket_list')

    context = {
            'form' : form,
            'ticket' : ticket,
        }        
    return render(request, 'user/user_update_ticket.html', context)




#user delete ticket
@login_required(login_url = 'user_login')
def user_delete_ticket(request,id):
    ticket = Ticket.objects.filter(id=id)   
    ticket.delete()  
    return redirect('user_ticket_list')



 