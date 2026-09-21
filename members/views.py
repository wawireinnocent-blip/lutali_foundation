from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from members.models import Member
from finance.models import Billing, Payment, Expense, Welfare
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_view(request):
    error = None
    if request.method == 'POST':
        phone = request.POST.get('phone','').strip()
        mno = request.POST.get('member_no','').strip().upper()
        try:
            m = Member.objects.get(phone=phone, member_no=mno)
            # Auto fix user link + password = member_no
            user, _ = User.objects.get_or_create(username=mno)
            user.set_password(mno)
            user.save()
            if not m.user or m.user.username!= mno:
                m.user = user
                m.save()
            login(request, user)
            if m.is_admin:
                return redirect('admin_dashboard')
            return redirect('member_dashboard')
        except Member.DoesNotExist:
            error = "Invalid Phone or Member No"
    return render(request, 'login.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def admin_dashboard(request):
    try:
        member = Member.objects.get(user=request.user)
    except:
        member = Member.objects.filter(is_admin=True).first()
    if not member.is_admin:
        return redirect('member_dashboard')
    total_members = Member.objects.count()
    active_count = Member.objects.filter(status='active').count()
    inactive_count = Member.objects.filter(status='inactive').count()
    total_expected = Billing.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_paid = Payment.objects.filter(status='verified').aggregate(Sum('amount'))['amount__sum'] or 0
    exp = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    wel = Welfare.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    foundation_cash = total_paid - exp - wel
    pending = Payment.objects.filter(status='pending').order_by('-date')
    members = Member.objects.all().order_by('member_no')
    return render(request, 'admin_dashboard.html', {
        'member': member, 'total_members': total_members, 'active_count': active_count,
        'inactive_count': inactive_count, 'total_expected': total_expected,
        'total_paid': total_paid, 'foundation_cash': foundation_cash,
        'pending': pending, 'members': members
    })

@login_required
def member_dashboard(request):
    try:
        member = Member.objects.get(user=request.user)
    except:
        return redirect('login')
    billings = Billing.objects.filter(member=member)
    payments = Payment.objects.filter(member=member).order_by('-date')
    expected = billings.aggregate(Sum('amount'))['amount__sum'] or 0
    paid = payments.filter(status='verified').aggregate(Sum('amount'))['amount__sum'] or 0
    total_paid_all = Payment.objects.filter(status='verified').aggregate(Sum('amount'))['amount__sum'] or 0
    exp = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    wel = Welfare.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    foundation_cash = total_paid_all - exp - wel
    balance = expected - paid
    return render(request, 'member_dashboard.html', {
        'member': member, 'billings': billings, 'payments': payments,
        'expected': expected, 'paid': paid, 'balance': balance,
        'foundation_cash': foundation_cash
    })

def bill_monthly(request):
    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')
        for m in Member.objects.filter(status='active'):
            if not Billing.objects.filter(member=m, billing_type='monthly', month=month, year=year).exists():
                Billing.objects.create(member=m, billing_type='monthly', amount=200, month=month, year=year)
    return redirect('admin_dashboard')

def add_member(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        mno = request.POST.get('member_no').upper()
        status = request.POST.get('status')
        user = User.objects.create_user(username=mno, password=mno)
        Member.objects.create(user=user, full_name=full_name, member_no=mno, phone=phone, status=status)
    return redirect('admin_dashboard')

def manual_payment(request):
    if request.method == 'POST':
        mid = request.POST.get('member_id')
        code = request.POST.get('mpesa_code')
        amount = request.POST.get('amount')
        m = Member.objects.get(id=mid)
        Payment.objects.create(member=m, mpesa_code=code.upper(), amount=amount, status='verified')
    return redirect('admin_dashboard')

def verify_payment(request, pid):
    p = get_object_or_404(Payment, id=pid)
    p.status = 'verified'
    p.save()
    return redirect('admin_dashboard')

def decline_payment(request, pid):
    p = get_object_or_404(Payment, id=pid)
    p.status = 'declined'
    p.save()
    return redirect('admin_dashboard')