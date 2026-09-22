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
    from django.http import HttpResponse

def restore_all_now(request):
    from .models import Member
    data=[
    {'name':'ISAAC FRED','member_number':'LUT-001','phone_number':'0768760386','status':'ACTIVE'},
    {'name':'Esther Luchivia','member_number':'LUT-002','phone_number':'0792967633','status':'ACTIVE'},
    {'name':'Ajella Mulari','member_number':'LUT-003','phone_number':'0759531836','status':'ACTIVE'},
    {'name':'INNOCENT WAWIRE','member_number':'LUT-004','phone_number':'0703416356','status':'ACTIVE'},
    {'name':'Laban Fula','member_number':'LUT-005','phone_number':'0111410769','status':'ACTIVE'},
    {'name':'KenPeter Muchika','member_number':'LUT-006','phone_number':'0768075466','status':'ACTIVE'},
    {'name':'Melvin Barasa','member_number':'LUT-007','phone_number':'0797969333','status':'ACTIVE'},
    {'name':'Mildred Lumbasi','member_number':'LUT-008','phone_number':'0707397500','status':'ACTIVE'},
    {'name':'Leah Juma','member_number':'LUT-009','phone_number':'0701434949','status':'ACTIVE'},
    {'name':'Yvonne Kharinda','member_number':'LUT-010','phone_number':'0759221476','status':'ACTIVE'},
    {'name':'Christine Zipporah','member_number':'LUT-011','phone_number':'0742023615','status':'ACTIVE'},
    {'name':'Alex Koikoi','member_number':'LUT-012','phone_number':'0706313051','status':'ACTIVE'},
    {'name':'Joshua Sindani','member_number':'LUT-013','phone_number':'0791279560','status':'ACTIVE'},
    {'name':'Emmanuel Sunguti','member_number':'LUT-014','phone_number':'0727994764','status':'ACTIVE'},
    {'name':'Cedrick Chivuyi','member_number':'LUT-015','phone_number':'0705890849','status':'ACTIVE'},
    {'name':'Mildred Nekesa','member_number':'LUT-016','phone_number':'0713364628','status':'ACTIVE'},
    {'name':'Burntone Kulova','member_number':'LUT-017','phone_number':'0700602172','status':'ACTIVE'},
    {'name':'Isaiah Wete','member_number':'LUT-018','phone_number':'0758795051','status':'ACTIVE'},
    {'name':'Austin Mando','member_number':'LUT-019','phone_number':'0715244622','status':'ACTIVE'},
    {'name':'Ali Kibaya','member_number':'LUT-020','phone_number':'0798911493','status':'ACTIVE'},
    {'name':'Philemon Tom','member_number':'LUT-021','phone_number':'0748343436','status':'ACTIVE'},
    {'name':'Nicole Nakhumicha','member_number':'LUT-022','phone_number':'0796610007','status':'INACTIVE'},
    {'name':'Mercyline Mutenyo','member_number':'LUT-023','phone_number':'0707828521','status':'ACTIVE'},
    {'name':'Salome Salim','member_number':'LUT-024','phone_number':'0795983430','status':'ACTIVE'},
    {'name':'Leah Salim','member_number':'LUT-025','phone_number':'0729010826','status':'ACTIVE'},
    {'name':'John Museve','member_number':'LUT-026','phone_number':'0798709891','status':'ACTIVE'},
    {'name':'Esther Kharinda','member_number':'LUT-027','phone_number':'0707277721','status':'ACTIVE'},
    {'name':'Gloria Imbiakha','member_number':'LUT-028','phone_number':'0743166089','status':'INACTIVE'},
    {'name':'Daniel Solomon','member_number':'LUT-029','phone_number':'0758570045','status':'ACTIVE'},
    {'name':'Elizabeth Muhonja','member_number':'LUT-030','phone_number':'0795313500','status':'ACTIVE'},
    {'name':'Gelda Weyala','member_number':'LUT-031','phone_number':'0712694179','status':'ACTIVE'},
    {'name':'Yvonne Mwenesi','member_number':'LUT-032','phone_number':'0787849794','status':'INACTIVE'},
    ]
    for m in data:
        Member.objects.update_or_create(member_number=m['member_number'], defaults=m)
    return HttpResponse(f"✅ WOTE 32 WAMERUDI! <br><br><a href='/admin-dashboard/'>Fungua Dashboard Sasa - Utaona 32</a>")

def member_report_pdf(request, member_id):
    return HttpResponse(f"PDF Report - Member {member_id}")

def my_report_pdf(request):
    return HttpResponse("PDF Report - My Report")
