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
            'earnings':['exact'],
        }

class PayrollFilter(django_filters.FilterSet):
    release_year = django_filters.NumberFilter(field_name='date', lookup_expr='year')
    class Meta:
        model = Payroll
        fields = {
            'id': ['exact'],
            'salary': ['exact'],

        }