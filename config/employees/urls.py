from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('list/', views.employee_list, name='employee_list'),
    path('create/', views.employee_create, name='employee_create'),
    path('<int:pk>/', views.employee_detail, name='employee_detail'),
    path('<int:pk>/update/', views.employee_update, name='employee_update'),
    path('<int:pk>/delete/', views.employee_delete, name='employee_delete'),
]
