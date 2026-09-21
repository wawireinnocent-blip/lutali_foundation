from django.urls import path
from . import views

urlpatterns = [
    path('submit-payment/', views.submit_payment, name='submit_payment'),
    path('add-welfare/', views.add_welfare, name='add_welfare'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('report-member/<int:member_id>/', views.report_member, name='report_member'),
    path('report-foundation/', views.report_foundation, name='report_foundation'),
    path('create-meeting/', views.create_meeting, name='create_meeting'),
]