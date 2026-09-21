from django.contrib import admin
from django.urls import path
from members.views import (
    login_view,
    admin_dashboard,
    member_dashboard,
    add_member,
    logout_view,
    fix_members,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('member-dashboard/', member_dashboard, name='member_dashboard'),
    path('add-member/', add_member, name='add_member'),
    path('fix-members/', fix_members, name='fix_members'),
]