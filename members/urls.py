from django.urls import path
from . import views
urlpatterns = [
    path('', views.login_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('member-dashboard/', views.member_dashboard, name='member_dashboard'),
    path('bill-monthly/', views.bill_monthly, name='bill_monthly'),
    path('create-welfare/', views.create_welfare, name='create_welfare'),
    path('create-meeting/', views.create_meeting, name='create_meeting'),
    path('attendance/<int:meeting_id>/', views.mark_attendance, name='attendance'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('add-payment-manual/', views.add_payment_manual, name='add_payment_manual'),
    path('member-payment/', views.member_payment, name='member_payment'),
    path('verify-payment/<int:pid>/<str:action>/', views.verify_payment, name='verify_payment'),
    path('seed-now/', views.seed_now, name='seed_now'),
    path('reports/foundation-pdf/', views.foundation_pdf, name='foundation_pdf'),
    path('reports/member-pdf/<int:member_id>/', views.member_pdf, name='member_pdf'),
    path('logout/', views.logout_view, name='logout'),
]
