from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from.models import Member, Payment, Expense
import re

def login_view(request):
    if request.method == 'POST':
        member_no = request.POST.get('member_number', '').strip()
        phone = request.POST.get('phone_number', '').strip()

        # Check if admin trying to login
        from django.contrib.auth.models import User
        user = authenticate(request, username=member_no, password=phone)
        if user and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')

        # Check member login
        try:
            member = Member.objects.get(member_number=member_no)
            # Simple check - phone as password
            if re.sub(r'[^0-9]','', member.phone_number) == re.sub(r'[^0-9]','', phone):
                request.session['member_id'] = member.id
                request.session['member_number'] = member.member_number
                return redirect('member_dashboard')
            else:
                messages.error(request, "Wrong phone number")
        except Member.DoesNotExist:
            messages.error(request, "Member not found")

    return render(request, 'members/login.html')

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('login')

def admin_dashboard(request):
    # Allow both superuser and member session for admin
    members = Member.objects.all().order_by('member_number')
    total_members = members.count()
    active = members.filter(is_active=True).count()
    inactive = total_members - active

    total_expected = total_members * 100
    total_paid = sum([m.total_paid() for m in members]) if hasattr(members.first(), 'total_paid') else 0
    balance = total_expected - total_paid if total_paid else total_expected

    context = {
        'members': members,
        'total_members': total_members,
        'active': active,
        'inactive': inactive,
        'total_expected': total_expected,
        'balance': balance,
    }
    return render(request, 'members/admin_dashboard.html', context)

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
            Member.objects.create(
                name=name,
                member_number=m_no,
                phone_number=re.sub(r'[^0-9]','', phone),
                is_active=True
            )
            messages.success(request, f"{name} added and billed 100!")
        return redirect('admin_dashboard')
    return render(request, 'members/add_member.html')

def submit_payment(request):
    # your existing payment logic
    return redirect('member_dashboard')

def approve_payment(request, payment_id):
    return redirect('admin_dashboard')

def foundation_report(request):
    return render(request, 'members/report.html')

# ✅✅✅ HII NDIO FIX YA WOTE 32 - ITA-RUN UKI-FUNGUA /fix-members/
def fix_members(request):
    import openpyxl
    from.models import Member

    try:
        wb = openpyxl.load_workbook("PHONE_NUMBERS.xlsx")
        ws = wb.active
        added = 0
        logs = []
        for row in ws.iter_rows(min_row=2, values_only=True):
            if not row or not row[0]:
                continue
            name = str(row[0]).strip()
            m_no = str(row[1]).strip()
            phone = re.sub(r'[^0-9]','', str(row[2] or ''))
            status = str(row[3] or 'ACTIVE').strip().upper()

            if not Member.objects.filter(member_number=m_no).exists():
                Member.objects.create(
                    name=name,
                    member_number=m_no,
                    phone_number=phone,
                    is_active=(status == 'ACTIVE')
                )
                added += 1
                logs.append(f"{m_no} - {name}")

        total = Member.objects.count()
        html = f"<h2>✅ Done! Added {added} new members</h2><h3>Total now: {total} / 32</h3><p>" + "<br>".join(logs) + "</p><br><a href='/admin-dashboard/' style='padding:10px 20px; background:green; color:white; text-decoration:none;'>Go to Dashboard</a>"
        return HttpResponse(html)
    except Exception as e:
        return HttpResponse(f"<h2>❌ Error: {e}</h2><p>Check if PHONE_NUMBERS.xlsx is uploaded to GitHub</p>")