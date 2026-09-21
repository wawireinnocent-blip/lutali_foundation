from django.contrib import admin
from django.urls import path
from members import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('member-dashboard/', views.member_dashboard, name='member_dashboard'),
    path('add-member/', views.add_member, name='add_member'),
    path('bill-monthly/', views.bill_monthly, name='bill_monthly'),
    path('add-manual-payment/', views.add_manual_payment, name='add_manual_payment'),
    path('member-submit/', views.member_submit_payment, name='member_submit_payment'),
    path('verify/<int:pk>/', views.verify_payment, name='verify_payment'),
    path('decline/<int:pk>/', views.decline_payment, name='decline_payment'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('add-welfare/', views.add_welfare, name='add_welfare'),
    path('create-meeting/', views.create_meeting, name='create_meeting'),
    path('mark-attendance/<int:meeting_id>/', views.mark_attendance, name='mark_attendance'),
    path('report/foundation-pdf/', views.foundation_report_pdf, name='foundation_report_pdf'),
    path('report/member-pdf/<int:member_id>/', views.member_report_pdf, name='member_report_pdf'),
    path('report/my-report-pdf/', views.my_report_pdf, name='my_report_pdf'),
    path('logout/', views.logout_view, name='logout'),
]