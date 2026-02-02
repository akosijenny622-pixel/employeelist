"""
Django management command to create a superuser with environment variables.
Usage: python manage.py create_admin
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os


class Command(BaseCommand):
    help = 'Creates a superuser from environment variables or prompts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Admin username',
        )
        parser.add_argument(
            '--email',
            type=str,
            help='Admin email',
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Admin password',
        )

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Get credentials from options, environment variables, or defaults
        username = options.get('username') or os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = options.get('email') or os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = options.get('password') or os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Superuser "{username}" already exists!')
            )
            return
        
        # If no password provided, show error
        if not password:
            self.stdout.write(
                self.style.ERROR(
                    'Password is required! Provide via --password argument or '
                    'DJANGO_SUPERUSER_PASSWORD environment variable'
                )
            )
            return
        
        # Create the superuser
        try:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            # Set role to 'admin' for clarity (even though is_superuser=True is enough)
            user.role = 'admin'
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Superuser "{username}" created successfully!'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {str(e)}')
            )
