from django.urls import path
from . import views
urlpatterns=[
    path('',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('admin-dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('member-dashboard/',views.member_dashboard,name='member_dashboard'),
    path('bill-monthly/',views.bill_monthly,name='bill_monthly'),
    path('add-member/',views.add_member,name='add_member'),
    path('manual-payment/',views.manual_payment,name='manual_payment'),
    path('verify/<int:pid>/',views.verify_payment,name='verify_payment'),
    path('decline/<int:pid>/',views.decline_payment,name='decline_payment'),
]