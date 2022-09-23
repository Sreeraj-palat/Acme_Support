
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect

def allowed_users(allowed_role=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            role = None
            if request.user.role.exists():
                role = request.user.role.all()[0].name

            if role in allowed_role:
                return view_func(request, *args, **kwargs) 
            else:
                return HttpResponse('not authorised')
        return wrapper_func
    return decorator               