from django.contrib import admin
from django.urls import path, include
from members.views import login_view, logout_view, admin_dashboard, member_dashboard, bill_monthly, add_member, manual_payment, verify_payment, decline_payment

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('member-dashboard/', member_dashboard, name='member_dashboard'),
    path('bill-monthly/', bill_monthly, name='bill_monthly'),
    path('add-member/', add_member, name='add_member'),
    path('manual-payment/', manual_payment, name='manual_payment'),
    path('verify/<int:pid>/', verify_payment, name='verify_payment'),
    path('decline/<int:pid>/', decline_payment, name='decline_payment'),
    path('finance/', include('finance.urls')),
]