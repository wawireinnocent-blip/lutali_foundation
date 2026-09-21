from django.contrib import admin
from django.urls import path
from members.views import (
    login_view,
    admin_dashboard,
    member_dashboard,
    add_member,
    logout_view,
    fix_members,
    submit_payment,
    approve_payment,
    foundation_report
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth - login yako iko kwa root "/" ndio maana /login/ inapea 404
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Dashboards
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('member-dashboard/', member_dashboard, name='member_dashboard'),

    # Member actions
    path('add-member/', add_member, name='add_member'),
    path('submit-payment/', submit_payment, name='submit_payment'),
    path('approve-payment/<int:payment_id>/', approve_payment, name='approve_payment'),
    path('foundation-report/', foundation_report, name='foundation_report'),

    # ✅ FIX LINK - hii ndio ita-import 30 members wali-baki
    path('fix-members/', fix_members, name='fix_members'),
]