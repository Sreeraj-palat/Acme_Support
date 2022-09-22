from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from accounts.models import Account


# Create your views here.




@login_required(login_url = 'master_login')
def master_dashboard(request):
    return render(request, 'master/master_dashboard.html')




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
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('master_login')    



