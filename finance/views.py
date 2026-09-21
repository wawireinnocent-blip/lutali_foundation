from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from members.models import Member
from finance.models import Billing, Payment, Expense, Welfare
from django.db.models import Sum
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
import random, string, os
from django.conf import settings

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

def get_logo_path():
    possible = [
        os.path.join(settings.BASE_DIR, 'static', 'logo.png'),
        os.path.join(settings.BASE_DIR, 'staticfiles', 'logo.png'),
        os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.png'),
        'static/logo.png',
        'staticfiles/logo.png',
    ]
    for p in possible:
        if os.path.exists(p):
            return p
    return None

@login_required
def create_meeting(request):
    return redirect('admin_dashboard')

@login_required
def submit_payment(request):
    if request.method == 'POST':
        code = request.POST.get('mpesa_code','').strip().upper()
        amount = request.POST.get('amount')
        try:
            member = Member.objects.get(user=request.user)
            Payment.objects.create(member=member, mpesa_code=code, amount=amount, status='pending')
        except:
            pass
    return redirect('member_dashboard')

@login_required
def add_welfare(request):
    if request.method == 'POST':
        mno = request.POST.get('member_no','').strip().upper()
        amount = request.POST.get('amount')
        try:
            m = Member.objects.get(member_no=mno)
            Welfare.objects.create(member=m, amount=amount, description=f"Welfare to {mno}")
        except:
            pass
    return redirect('admin_dashboard')

@login_required
def add_expense(request):
    if request.method == 'POST':
        desc = request.POST.get('desc')
        amount = request.POST.get('amount')
        Expense.objects.create(description=desc, amount=amount)
    return redirect('admin_dashboard')

def draw_header(p, w, h, title, subtitle):
    # Green header bar
    p.setFillColor(colors.HexColor("#0a7a3a"))
    p.rect(0, h-90, w, 90, fill=1, stroke=0)
    # Logo
    logo = get_logo_path()
    if logo:
        try:
            p.drawImage(logo, 40, h-75, width=50, height=50, mask='auto')
        except:
            pass
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(105, h-45, "LUTALI FOUNDATION")
    p.setFont("Helvetica", 8)
    p.drawString(105, h-58, subtitle)
    p.drawString(105, h-70, "Till: 1647509 | Reg: KES 100 | Monthly: KES 200 | lutalifoundation.org")
    # Title on right
    p.setFont("Helvetica-Bold", 11)
    p.drawRightString(w-40, h-45, title)

@login_required
def report_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    try:
        req_member = Member.objects.get(user=request.user)
        if not req_member.is_admin and req_member.id!= member.id:
            member = req_member
    except:
        pass
    billings = Billing.objects.filter(member=member).order_by('year','month')
    payments = Payment.objects.filter(member=member).order_by('-date')
    expected = billings.aggregate(Sum('amount'))['amount__sum'] or 0
    paid_verified = payments.filter(status='verified').aggregate(Sum('amount'))['amount__sum'] or 0
    paid_pending = payments.filter(status='pending').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = expected - paid_verified
    total_paid_all = Payment.objects.filter(status='verified').aggregate(Sum('amount'))['amount__sum'] or 0
    exp = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    wel = Welfare.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    foundation_cash = total_paid_all - exp - wel

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{member.member_no}_Statement.pdf"'
    p = canvas.Canvas(response, pagesize=A4)
    w, h = A4
    draw_header(p, w, h, "MEMBER STATEMENT", f"Statement for {member.member_no} | {datetime.now().strftime('%d %b %Y')}")

    y = h-120
    p.setFillColor(colors.black)
    p.setFont("Helvetica-Bold", 11)
    p.drawString(40, y, f"{member.full_name}")
    p.setFont("Helvetica", 9)
    p.drawString(40, y-14, f"{member.member_no} | {member.phone} | Status: {member.status.upper()}")
    # Status box
    p.setFillColor(colors.HexColor("#f3f4f6"))
    p.roundRect(w-180, y-20, 140, 35, 6, fill=1, stroke=0)
    p.setFillColor(colors.black)
    p.setFont("Helvetica-Bold", 8)
    p.drawString(w-170, y-5, f"BALANCE / DENI")
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.red if balance>0 else colors.HexColor("#0a7a3a"))
    p.drawString(w-170, y-18, f"KES {balance}")
    p.setFillColor(colors.black)

    y -= 50
    # Summary table
    p.setFillColor(colors.HexColor("#111827"))
    p.rect(40, y-25, w-80, 25, fill=1, stroke=0)
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 8)
    p.drawString(50, y-12, "TOTAL EXPECTED")
    p.drawString(160, y-12, "VERIFIED PAID")
    p.drawString(260, y-12, "PENDING")
    p.drawString(340, y-12, "FOUNDATION CASH")
    y -= 25
    p.setFillColor(colors.HexColor("#f9fafb"))
    p.rect(40, y-18, w-80, 18, fill=1, stroke=0)
    p.setFillColor(colors.black)
    p.setFont("Helvetica", 8)
    p.drawString(50, y-8, f"KES {expected}")
    p.drawString(160, y-8, f"KES {paid_verified}")
    p.drawString(260, y-8, f"KES {paid_pending}")
    p.drawString(340, y-8, f"KES {foundation_cash}")
    y -= 35

    p.setFont("Helvetica-Bold", 10)
    p.drawString(40, y, "PAYMENT HISTORY - DETAILED")
    y -= 15
    p.setFont("Helvetica-Bold", 7)
    p.setFillColor(colors.HexColor("#f3f4f6"))
    p.rect(40, y-12, w-80, 14, fill=1, stroke=0)
    p.setFillColor(colors.black)
    p.drawString(45, y-4, "DATE")
    p.drawString(120, y-4, "MPESA CODE")
    p.drawString(220, y-4, "AMOUNT")
    p.drawString(300, y-4, "STATUS")
    y -= 18
    p.setFont("Helvetica", 7)
    for pay in payments:
        if y < 90:
            p.showPage()
            y = h-50
            draw_header(p, w, h, "MEMBER STATEMENT CONT.", f"{member.member_no}")
            y = h-120
        p.drawString(45, y, str(pay.date)[:19])
        p.drawString(120, y, pay.mpesa_code)
        p.drawString(220, y, f"KES {pay.amount}")
        p.drawString(300, y, pay.status.upper())
        y -= 10

    y -= 15
    p.setFont("Helvetica-Bold", 10)
    p.drawString(40, y, "BILLING / MADENI")
    y -= 12
    p.setFont("Helvetica", 7)
    for b in billings:
        if y < 90:
            p.showPage()
            y = h-50
        p.drawString(40, y, f"{b.billing_type} | {b.description} | {b.month}/{b.year} | KES {b.amount}")
        y -= 10

    p.setFont("Helvetica", 6)
    p.setFillColor(colors.grey)
    p.drawString(40, 40, f"Generated: {datetime.now()} | {generate_code()} | This document is system generated and confidential - LUTALI FOUNDATION")
    p.drawRightString(w-40, 40, f"Till 1647509")
    p.showPage()
    p.save()
    return response

@login_required
def report_foundation(request):
    members = Member.objects.all().order_by('member_no')
    payments = Payment.objects.all().order_by('-date')
    billings = Billing.objects.all()
    expenses = Expense.objects.all().order_by('-date')
    welfares = Welfare.objects.all().order_by('-date')
    total_expected = billings.aggregate(Sum('amount'))['amount__sum'] or 0
    total_paid_verified = payments.filter(status='verified').aggregate(Sum('amount'))['amount__sum'] or 0
    exp_total = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    wel_total = welfares.aggregate(Sum('amount'))['amount__sum'] or 0
    foundation_cash = total_paid_verified - exp_total - wel_total
    total_balance = total_expected - total_paid_verified

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Foundation_Report_{datetime.now().date()}.pdf"'
    p = canvas.Canvas(response, pagesize=A4)
    w, h = A4
    draw_header(p, w, h, "FOUNDATION REPORT", f"Complete Financial Report | {datetime.now().strftime('%d %b %Y')} | Members: {members.count()}")

    y = h-120
    p.setFillColor(colors.HexColor("#111827"))
    p.setFont("Helvetica-Bold", 9)
    p.drawString(40, y, "SUMMARY")
    y -= 8
    # Summary boxes
    p.setFillColor(colors.HexColor("#f9fafb"))
    p.rect(40, y-45, w-80, 45, fill=1, stroke=0)
    p.setStrokeColor(colors.HexColor("#e5e7eb"))
    p.rect(40, y-45, w-80, 45, fill=0, stroke=1)
    p.setFillColor(colors.black)
    p.setFont("Helvetica", 8)
    p.drawString(50, y-5, f"Total Expected: KES {total_expected}")
    p.drawString(200, y-5, f"Total Paid (Verified): KES {total_paid_verified}")
    p.drawString(380, y-5, f"Total Deni: KES {total_balance}")
    p.drawString(50, y-20, f"Expenses: KES {exp_total}")
    p.drawString(200, y-20, f"Welfare: KES {wel_total}")
    p.setFont("Helvetica-Bold", 9)
    p.setFillColor(colors.HexColor("#0a7a3a"))
    p.drawString(380, y-20, f"CASH: KES {foundation_cash}")
    p.setFillColor(colors.black)
    y -= 65

    p.setFont("Helvetica-Bold", 10)
    p.drawString(40, y, "MEMBER BALANCES & MADENI ZA KILA MEMBER")
    y -= 12
    p.setFont("Helvetica-Bold", 6)
    p.setFillColor(colors.HexColor("#111827"))
    p.rect(40, y-12, w-80, 12, fill=1, stroke=0)
    p.setFillColor(colors.white)
    p.drawString(45, y-5, "NO")
    p.drawString(80, y-5, "NAME")
    p.drawString(200, y-5, "EXPECTED")
    p.drawString(260, y-5, "PAID")
    p.drawString(310, y-5, "DENI/BALANCE")
    p.drawString(380, y-5, "STATUS")
    y -= 18
    p.setFont("Helvetica", 6)
    p.setFillColor(colors.black)
    for m in members:
        if y < 90:
            p.showPage()
            y = h-50
            draw_header(p, w, h, "FOUNDATION REPORT CONT.", f"Members & Payments")
            y = h-120
        m_expected = Billing.objects.filter(member=m).aggregate(Sum('amount'))['amount__sum'] or 0
        m_paid = Payment.objects.filter(member=m, status='verified').aggregate(Sum('amount'))['amount__sum'] or 0
        m_balance = m_expected - m_paid
        p.drawString(45, y, m.member_no)
        p.drawString(80, y, m.full_name[:22])
        p.drawString(200, y, f"{m_expected}")
        p.drawString(260, y, f"{m_paid}")
        p.setFillColor(colors.red if m_balance>0 else colors.HexColor("#0a7a3a"))
        p.drawString(310, y, f"{m_balance}")
        p.setFillColor(colors.black)
        p.drawString(380, y, m.status.upper())
        y -= 9

    p.showPage()
    y = h-50
    draw_header(p, w, h, "FOUNDATION REPORT", "All Payments & Transactions")
    y = h-120
    p.setFont("Helvetica-Bold", 10)
    p.setFillColor(colors.black)
    p.drawString(40, y, "ALL PAYMENTS (Verified, Pending, Declined)")
    y -= 12
    p.setFont("Helvetica", 6)
    for pay in payments[:150]:
        if y < 90:
            p.showPage()
            y = h-50
        p.drawString(40, y, f"{str(pay.date)[:19]} | {pay.member.member_no} - {pay.member.full_name[:15]} | {pay.mpesa_code} | KES {pay.amount} | {pay.status.upper()}")
        y -= 8

    p.setFont("Helvetica", 6)
    p.setFillColor(colors.grey)
    p.drawString(40, 40, f"Generated: {datetime.now()} | Code: {generate_code()} | LUTALI FOUNDATION - Confidential Report")
    p.showPage()
    p.save()
    return response