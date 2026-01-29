from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Employee

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}))
    last_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        # default new signups to employee role
        user.role = 'employee'
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.email = self.cleaned_data.get('email', '')
        user.phone = self.cleaned_data.get('phone', '')
        if commit:
            user.save()
        return user

class EmployeeForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = Employee
        fields = ['employee_id', 'department', 'position', 'hire_date', 'salary', 'status', 'address']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.instance_user = kwargs.pop('instance_user', None)
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['username'].initial = self.instance.user.username
            self.fields['phone'].initial = self.instance.user.phone
            self.fields['password'].required = False

    def save(self, commit=True):
        employee = super().save(commit=False)

        if self.instance.pk:
            user = self.instance.user
        else:
            user = User()
            user.role = 'employee'

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.phone = self.cleaned_data['phone']

        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])
        elif not self.instance.pk:
            user.set_password('changeme123')

        if commit:
            user.save()
            employee.user = user
            employee.save()

        return employee
