from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters,generics
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from .filtersSet import *
import datetime
import calendar
import random

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

# def add_months(sourcedate, months):
#     month  = sourcedate.month - 1 + months
#     year  = sourcedate.year + month // 12
#     month = month % 12 + 1
#     day  = min(sourcedate.day, calendar.monthrange(year,month)[1])
#     return datetime.date(year, month, day)
#
# end_date = datetime.date.today()
#
# class CreatePayRoll():
#     employees = Employee.objects.all()
#     for employee in employees:
#         print("employee", employee.user)
#         index=1
#         while True:
#             randomInt = random.randint(-5, 20)
#             actual_salary= round(employee.earnings+(employee.earnings/100)*randomInt,0)
#             print("Month:",add_months(employee.join_date ,index),':',employee.earnings,':',randomInt,':',type(int(actual_salary)))
#             index=index+1
#             # payroll=Payroll.objects.create(
#             #     name=employee,
#             #     salary=int(actual_salary),
#             #     date=add_months(employee.join_date ,index)
#             # )
#             if add_months(employee.join_date,index) >= datetime.date.today():
#                 break
#         print("--------------")


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    permission_classes=[IsAdminUser,]
    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filter_class = EmployeeFilter
    lookup_field = 'slug'
    ordering  = ['role']

    def create(self, request, *args, **kwargs):
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
        join_date = datetime.datetime.strptime(new_employee['join_date'][:10], "%Y-%M-%d")
        date_of_birth = datetime.datetime.strptime(new_employee['date_of_birth'][:10], "%Y-%M-%d")

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

class PayrollViewSet(viewsets.ModelViewSet):
    queryset = Payroll.objects.all()
    permission_classes=[IsAdminUser,]
    serializer_class = PayrollSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filter_class = PayrollFilter
    ordering = ['-date']


class PayrollViewSetAction(generics.ListCreateAPIView):
    queryset = Payroll.objects.all()
    permission_classes=[IsAdminUser,]
    serializer_class = PayrollSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filter_class = PayrollFilter
    lookup_field = 'name'
    ordering = ['-date']

    def get_queryset(self):
        slug = self.kwargs["pk"]
        employee = Employee.objects.get(slug=slug)
        queryset = Payroll.objects.filter(name = employee)
        return queryset


