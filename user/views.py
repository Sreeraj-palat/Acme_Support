from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from accounts.models import Account


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

