from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from.models import Member
import re

# LOGIN - Iko kwa root "/"
def login_view(request):
    if request.method == 'POST':
        m_no = request.POST.get('member_number','').strip()
        phone = request.POST.get('phone_number','').strip()

        # Admin login
        from django.contrib.auth import authenticate, login
        user = authenticate(request, username=m_no, password=phone)
        if user and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')

        # Member login
        try:
            member = Member.objects.get(member_number=m_no)
            clean_phone = re.sub(r'[^0-9]','', phone)
            db_phone = re.sub(r'[^0-9]','', member.phone_number or '')
            if clean_phone == db_phone or phone == member.phone_number:
                request.session['member_id'] = member.id
                return redirect('member_dashboard')
            else:
                messages.error(request, "Wrong phone")
        except Member.DoesNotExist:
            messages.error(request, "Member not found")

    return render(request, 'members/login.html')

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    request.session.flush()
    return redirect('login')

# ADMIN DASHBOARD - HAPA NDIO AUTO IMPORT YA 32
def admin_dashboard(request):
    # ===== AUTO FIX YA 32 MEMBERS - ITA-RUN UKIFUNGUA HII PAGE =====
    if Member.objects.count() < 32:
        import openpyxl
        try:
            wb = openpyxl.load_workbook("PHONE_NUMBERS.xlsx")
            ws = wb.active
            added = 0
            for row in ws.iter_rows(min_row=2, values_only=True):
                if not row or not row[0]:
                    continue
                name = str(row[0]).strip()
                m_no = str(row[1]).strip()
                phone = re.sub(r'[^0-9]','', str(row[2] or ''))
                status = str(row[3] or 'ACTIVE').upper()
                if not Member.objects.filter(member_number=m_no).exists():
                    Member.objects.create(
                        name=name,
                        member_number=m_no,
                        phone_number=phone,
                        is_active=(status=='ACTIVE')
                    )
                    added += 1
            print(f"AUTO ADDED {added} MEMBERS")
        except Exception as e:
            print(f"Auto import error: {e}")
    # ===== MWISHO WA AUTO FIX =====

    members = Member.objects.all().order_by('member_number')
    total_members = members.count()
    active = members.filter(is_active=True).count()

    return render(request, 'members/admin_dashboard.html', {
        'members': members,
        'total_members': total_members,
        'active': active,
        'inactive': total_members - active,
    })

def member_dashboard(request):
    member_id = request.session.get('member_id')
    if not member_id:
        return redirect('login')
    member = get_object_or_404(Member, id=member_id)
    return render(request, 'members/member_dashboard.html', {'member': member})

def add_member(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        m_no = request.POST.get('member_number')
        phone = request.POST.get('phone_number')
        if not Member.objects.filter(member_number=m_no).exists():
            Member.objects.create(name=name, member_number=m_no, phone_number=re.sub(r'[^0-9]','', phone), is_active=True)
            messages.success(request, f"{name} added!")
        return redirect('admin_dashboard')
    return render(request, 'members/add_member.html')

# Functions zingine ili zisilete error
def bill_monthly(request):
    return redirect('admin_dashboard')

def add_manual_payment(request):
    return redirect('admin_dashboard')

def member_submit_payment(request):
    return redirect('member_dashboard')

def verify_payment(request, pk):
    return redirect('admin_dashboard')

def decline_payment(request, pk):
    return redirect('admin_dashboard')

def add_expense(request):
    return redirect('admin_dashboard')

def add_welfare(request):
    return redirect('admin_dashboard')

def create_meeting(request):
    return redirect('admin_dashboard')

def mark_attendance(request, meeting_id):
    return redirect('admin_dashboard')

def foundation_report_pdf(request):
    return HttpResponse("PDF Report - Foundation")

def member_report_pdf(request, member_id):
    return HttpResponse(f"PDF Report - Member {member_id}")

def my_report_pdf(request):
    return HttpResponse("PDF Report - My Report")