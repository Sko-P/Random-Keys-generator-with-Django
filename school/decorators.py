from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    
    def wrapper_func(request, *args, **kwargs):
        if(request.user.is_authenticated):
            return redirect('main')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            #if(view_func.__name__ == "home"):
                
            
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not allowed') #can be replaced by a return redirect
        return wrapper_func
    return decorator


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

         #if the access is for home

        if(group == 'students'):
            return redirect('student')
                
        if(group == 'admin'):
            return view_func(request, *args, **kwargs)

    return wrapper_function