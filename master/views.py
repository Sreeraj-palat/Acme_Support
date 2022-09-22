from django.shortcuts import render

# Create your views here.
def master_dashboard(request):
    return render(request, 'master/master_dashboard.html')
