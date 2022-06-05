import django_filters
from django.db.models import Q

from employee.models import *
from .serializers import *
from rest_framework import viewsets


class EmployeeFilter(django_filters.FilterSet):
    join_date = django_filters.NumberFilter(field_name='join_date', lookup_expr='month')
    birthday = django_filters.NumberFilter(field_name='date_of_birth', lookup_expr='month')
    role = django_filters.CharFilter(field_name='role__title',lookup_expr='iexact' )
    first_name = django_filters.CharFilter(field_name='user__first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='user__last_name', lookup_expr='icontains')
    user = django_filters.CharFilter(field_name='user', method='search_by_full_name')

    def search_by_full_name(self,qs,name, value):
        qs = User.objects.all()
        for term in value.split():
            qs = qs.filter(Q(first_name__icontains=term) | Q(last_name__icontains=term))
        employee = Employee.objects.filter(user__in= qs)
        return employee
    class Meta:
        model = Employee
        fields = {
            'role': ['exact'],
            'group': ['exact'],
            'earnings':['exact'],
            'user':['exact'],
        }

class PayrollFilter(django_filters.FilterSet):
    release_year = django_filters.NumberFilter(field_name='date', lookup_expr='year')
    class Meta:
        model = Payroll
        fields = {
            'id': ['exact'],
            'salary': ['exact'],

        }