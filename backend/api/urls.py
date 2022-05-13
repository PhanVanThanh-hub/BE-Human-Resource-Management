from rest_framework import routers
from django.urls import path,include
from employee.api.views import *
from rest_framework_simplejwt import views as jwt_views
from login.api.views import *

router = routers.DefaultRouter()
router.register('employee', EmployeeViewSet, basename="employee-view-set")
router.register('getRole', RoleViewSet, basename="role-view-set")
router.register('group', GroupViewSet, basename="group-view-set")
router.register('payroll', PayrollViewSet, basename="payroll-view-set")
urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UsersViewSet.as_view()),
    path('decentralization/',decentralizationUser.as_view() ,),
    path('payroll/<pk>/', PayrollViewSetAction.as_view()),
    # path('create_payroll',CreatePayRoll)
]

urlpatterns += router.urls