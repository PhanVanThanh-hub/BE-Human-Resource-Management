import django_filters
from employee.models import *
from .serializers import *
from rest_framework import viewsets


class EmployeeFilter(django_filters.FilterSet):
    class Meta:
        model = Employee
        fields = {
            'role': ['exact'],
            'group': ['exact'],
        }

class PayrollFilter(django_filters.FilterSet):
    class Meta:
        model = Payroll
        fields = {
            'id': ['exact'],
            'date': ['exact'],
            'salary': ['exact'],
        }