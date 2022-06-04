from django.contrib.auth.models import User
from rest_framework import  serializers
from employee.models import *

class EmployeeSerializer(serializers.ModelSerializer):
    role = serializers.ReadOnlyField(source='role.title')
    group = serializers.ReadOnlyField(source='group.name_group')
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    class Meta:
        model = Employee
        fields = "__all__"
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }

class EmployeeStaffSerializer(serializers.ModelSerializer):
    role = serializers.ReadOnlyField(source='role.title')
    email = serializers.CharField(source="user.email")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    class Meta:
        model = Employee
        exclude = ['earnings','slug','user','group']
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }








class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

class PayrollSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='name.slug')
    class Meta:
        model = Payroll
        fields = "__all__"
