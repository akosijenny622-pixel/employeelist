from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from employees.models import Employee, User
from employees.forms import LoginForm, SignupForm

def login_view(request):
    # Do not automatically redirect authenticated users away from the login
    # page. Instead render the login page and show an informational message so
    # users who open the site still land on the login page.
    already_logged_in = request.user.is_authenticated

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}.")
            # Respect next parameter for redirects
            next_url = request.GET.get('next') or request.POST.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')
    else:
        form = LoginForm()

    return render(request, 'security_management/pages/login.html', {
        'form': form,
        'already_logged_in': already_logged_in,
    })


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically create Employee profile for new user
            import datetime
            # Generate a unique employee_id (e.g., EMP + user pk)
            employee_id = f"EMP{user.pk:04d}"
            Employee.objects.create(
                user=user,
                employee_id=employee_id,
                department='IT',  # default, can be changed later
                position='New Employee',
                hire_date=datetime.date.today(),
                salary=0,
                status='active',
                address='',
            )
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('security_management:login')
    else:
        form = SignupForm()

    return render(request, 'security_management/pages/signup.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('security_management:login')

# Create your views here.
