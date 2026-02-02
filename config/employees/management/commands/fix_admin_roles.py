"""
Django management command to fix role field for all superusers.
This ensures all admin users have role='admin' in the database.
Usage: python manage.py fix_admin_roles
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Fix role field for all superusers to ensure they display as Admin'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Find all superusers or staff users
        admin_users = User.objects.filter(is_superuser=True) | User.objects.filter(is_staff=True)
        
        updated_count = 0
        for user in admin_users:
            if user.role != 'admin':
                user.role = 'admin'
                user.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Updated role for user: {user.username}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'→ User {user.username} already has admin role')
                )
        
        if updated_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'\n✓ Total users updated: {updated_count}')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('\n✓ All admin users already have correct role!')
            )
