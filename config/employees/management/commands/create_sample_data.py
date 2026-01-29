from django.core.management.base import BaseCommand
from employees.models import User, Employee
from django.utils import timezone
import datetime

class Command(BaseCommand):
    help = 'Create sample employee data'

    def handle(self, *args, **options):
        # Create admin employee profile if it doesn't exist
        admin_user = User.objects.filter(username='admin').first()
        if admin_user and not hasattr(admin_user, 'employee_profile'):
            employee = Employee.objects.create(
                user=admin_user,
                employee_id='EMP0001',
                department='IT',
                position='System Administrator',
                hire_date=datetime.date(2023, 1, 15),
                salary=75000.00,
                status='active',
                address='123 Main Street, Technology City, TC 12345'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created employee profile for {admin_user.username}')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Admin user not found or already has employee profile')
            )

        # Create additional sample employees
        sample_employees = [
            {
                'username': 'john_doe',
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@company.com',
                'phone': '+1-555-0123',
                'role': 'employee',
                'employee_id': 'EMP0002',
                'department': 'HR',
                'position': 'Human Resources Specialist',
                'hire_date': datetime.date(2023, 3, 20),
                'salary': 55000.00,
                'status': 'active',
                'address': '456 Oak Avenue, Business District, BD 67890'
            },
            {
                'username': 'jane_smith',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'email': 'jane.smith@company.com',
                'phone': '+1-555-0124',
                'role': 'employee',
                'employee_id': 'EMP0003',
                'department': 'FIN',
                'position': 'Financial Analyst',
                'hire_date': datetime.date(2023, 2, 10),
                'salary': 62000.00,
                'status': 'active',
                'address': '789 Pine Street, Finance Plaza, FP 11223'
            },
            {
                'username': 'bob_wilson',
                'first_name': 'Bob',
                'last_name': 'Wilson',
                'email': 'bob.wilson@company.com',
                'phone': '+1-555-0125',
                'role': 'employee',
                'employee_id': 'EMP0004',
                'department': 'MKT',
                'position': 'Marketing Manager',
                'hire_date': datetime.date(2022, 11, 5),
                'salary': 68000.00,
                'status': 'on_leave',
                'address': '321 Elm Drive, Marketing Center, MC 33445'
            }
        ]

        for emp_data in sample_employees:
            # Create user if doesn't exist
            user, created = User.objects.get_or_create(
                username=emp_data['username'],
                defaults={
                    'first_name': emp_data['first_name'],
                    'last_name': emp_data['last_name'],
                    'email': emp_data['email'],
                    'phone': emp_data['phone'],
                    'role': emp_data['role']
                }
            )
            
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {user.username}')

            # Create employee profile if doesn't exist
            employee, created = Employee.objects.get_or_create(
                user=user,
                defaults={
                    'employee_id': emp_data['employee_id'],
                    'department': emp_data['department'],
                    'position': emp_data['position'],
                    'hire_date': emp_data['hire_date'],
                    'salary': emp_data['salary'],
                    'status': emp_data['status'],
                    'address': emp_data['address']
                }
            )
            
            if created:
                self.stdout.write(f'Created employee profile: {employee.employee_id}')
            else:
                self.stdout.write(f'Employee profile already exists: {employee.employee_id}')

        self.stdout.write(
            self.style.SUCCESS('Sample data creation completed!')
        )