import os
import sys
import django

# Add the project path to sys.path
sys.path.append('c:/Users/Vergil/config/config')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from employees.models import Employee, User

print("=== Employee Data Verification ===")
print(f"Total Employees: {Employee.objects.count()}")
print(f"Total Users: {User.objects.count()}")
print()

# Check if admin has employee profile
admin_user = User.objects.filter(username='admin').first()
if admin_user:
    print(f"Admin User: {admin_user.username} ({admin_user.get_full_name()})")
    employee = Employee.objects.filter(user=admin_user).first()
    if employee:
        print(f"Admin Employee Profile: {employee.employee_id} - {employee.position}")
        print(f"Department: {employee.get_department_display()}")
        print(f"Status: {employee.get_status_display()}")
    else:
        print("No employee profile for admin user")
else:
    print("Admin user not found")

print()
print("=== All Employees ===")
for emp in Employee.objects.all():
    print(f"{emp.employee_id}: {emp.user.username} - {emp.position} ({emp.get_department_display()})")