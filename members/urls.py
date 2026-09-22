from django.urls import path
from. import views

urlpatterns = [
    path('', views.member_login, name='home'),
    path('member-login/', views.member_login, name='member_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('member-dashboard/', views.member_dashboard, name='member_dashboard'),
    path('logout/', views.member_logout, name='logout'),
    path('delete-member/<int:member_id>/', views.delete_member, name='delete_member'),
    path('import-now/', views.import_now, name='import_now'),
]
