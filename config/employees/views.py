from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Employee, User
from .forms import EmployeeForm

def is_admin(user):
    # treat both users with role 'admin' and Django superusers as admins
    return user.is_authenticated and (getattr(user, 'role', None) == 'admin' or getattr(user, 'is_superuser', False))

# Authentication views moved to security_management app

@login_required
def dashboard(request):
    # use the module-level is_admin(user) helper instead of calling a method
    # on the user object (which may not exist). This ensures admins render
    # the admin dashboard with the full employee list.
    if is_admin(request.user):
        # support search and filtering on the admin dashboard
        query = request.GET.get('q', '')
        department = request.GET.get('department', '')
        status = request.GET.get('status', '')

        employees = Employee.objects.select_related('user').all()

        if query:
            employees = employees.filter(
                Q(employee_id__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(position__icontains=query)
            )

        if department:
            employees = employees.filter(department=department)

        if status:
            employees = employees.filter(status=status)

        context = {
            'total_employees': Employee.objects.count(),
            'active_employees': Employee.objects.filter(status='active').count(),
            'departments': Employee.DEPARTMENT_CHOICES,
            'employees': employees,
            'query': query,
            'department': department,
            'status': status,
            'statuses': Employee.STATUS_CHOICES,
        }
        return render(request, 'employees/pages/admin_dashboard.html', context)
    else:
        # Some users (including superusers created via createsuperuser) may not have
        # an Employee record. Handle that gracefully instead of raising 404.
        employee = Employee.objects.filter(user=request.user).first()
        return render(request, 'employees/pages/employee_dashboard.html', {'employee': employee})

@login_required
@user_passes_test(is_admin)
def employee_list(request):
    # Employee list page removed — redirect to dashboard instead so the
    # list cannot be accessed directly. Templates that still link to
    # 'employee_list' will reach the dashboard.
    return redirect('dashboard')

@login_required
@user_passes_test(is_admin)
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            messages.success(request, f'Employee {employee.employee_id} created successfully.')
            return redirect('dashboard')
    else:
        form = EmployeeForm()

    return render(request, 'employees/pages/employee_form.html', {'form': form, 'action': 'Create'})

@login_required
@user_passes_test(is_admin)
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, 'employees/pages/employee_detail.html', {'employee': employee})

@login_required
@user_passes_test(is_admin)
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee, instance_user=employee.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Employee {employee.employee_id} updated successfully.')
            return redirect('employee_detail', pk=pk)
    else:
        form = EmployeeForm(instance=employee, instance_user=employee.user)

    return render(request, 'employees/pages/employee_form.html', {
        'form': form,
        'action': 'Update',
        'employee': employee
    })

@login_required
@user_passes_test(is_admin)
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        employee_id = employee.employee_id
        user = employee.user
        employee.delete()
        user.delete()
        messages.success(request, f'Employee {employee_id} deleted successfully.')
        return redirect('dashboard')

    return render(request, 'employees/pages/employee_confirm_delete.html', {'employee': employee})

# Create your views here.
