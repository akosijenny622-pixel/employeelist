from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Employee

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role']
    list_filter = ['role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone')}),
    )

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'get_full_name', 'department', 'position', 'status', 'hire_date']
    list_filter = ['department', 'status', 'hire_date']
    search_fields = ['employee_id', 'user__first_name', 'user__last_name', 'position']

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'

# Register your models here.
