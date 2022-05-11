from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.permissions import IsAdminUser
from .filtersSet import *
from datetime import datetime

s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'
def remove_accents(input_str):
	s :str = ''
	input_str.encode('utf-8')
	for c in input_str:
		if c in s1:
			s += s0[s1.index(c)]
		else:
			s += c
	return s

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    permission_classes=[IsAdminUser,]
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filter_class = EmployeeFilter
    ordering  = ['role']

    def create(self, request):
        new_employee = request.data
        username = remove_accents((new_employee['first_name']+new_employee['last_name']).replace(" ", ""))
        index = 1
        email_exists = User.objects.filter(email = new_employee['email']).count()
        if email_exists > 0:
            return JsonResponse({
                "message": "Email was Exists",
            })
        while True:
            try:
                user = User.objects.create_user(
                    username.lower()+str(index),
                    password="1234",
                    email=new_employee['email'],
                    first_name=new_employee['first_name'],
                    last_name=new_employee['last_name']
                )
            except:
                index = index+1;
            else:
                break
        print(user)
        group = Group.objects.get(id=new_employee['group'])
        role = Role.objects.get(id=new_employee['role'])
        join_date = datetime.strptime(new_employee['join_date'][:10], "%Y-%M-%d")
        date_of_birth = datetime.strptime(new_employee['date_of_birth'][:10], "%Y-%M-%d")

        employee = Employee.objects.create(
            user=user,
            date_of_birth=date_of_birth,
            earnings=new_employee['earnings'],
            ethnicity=new_employee['ethnicity'],
            full_time=new_employee['full_time'],
            group=group,
            role=role,
            join_date=join_date,
            location=new_employee['location'],
            phone=new_employee['phone'],
            sex=new_employee['sex']
        )
        employee.save()
        return JsonResponse({
            "message": "Done",
        })


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    permission_classes=[IsAdminUser,]
    serializer_class = RoleSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    permission_classes=[IsAdminUser,]
    serializer_class = GroupSerializer
    ordering = ['id']


