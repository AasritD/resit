from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegistrationForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('user_management:dashboard')
    else:
        form = LoginForm()
    return render(request, 'user_management/login.html', {
        'form': form,
        'is_register': False,   # login mode
    })

def logout_view(request):
    logout(request)
    return redirect('user_management:login')

@login_required
def dashboard_redirect_view(request):
    return render(request, 'user_management/dashboard.html')
    '''role = request.user.role
    if role == 'enduser':
        return redirect('/uploads/dashboard/')
    if role == 'aiengineer':
        return redirect('/inference/dashboard/')
    if role == 'admin':
        return redirect('/admin_dashboard/dashboard/')
    if role == 'finance':
        return redirect('/billing/dashboard/')
    return redirect('user_management:login')'''


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()      # new user with default ENDUSER role
            login(request, user)
            return redirect('user_management:dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'user_management/login.html', {
        'form': form,
        'is_register': True,    # register mode
    })
