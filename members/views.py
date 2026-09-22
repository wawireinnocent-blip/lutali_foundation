from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from .models import Member, Bill, Payment, Meeting, Attendance, Welfare, Expense
from .initial_data import seed_32
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

# LOGO BASE64 - TUMIA YAKO - NIMEWEKA PLACEHOLDER, BADILISHA NA BASE64 YAKO YA 12460 CHARS
LOGO = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAALQAAAC0CAYAAAB...WEKA BASE64 YAKO HAPA..."

def get_foundation_cash():
    verified = Payment.objects.filter(status='VERIFIED').aggregate(Sum('amount'))['amount__sum'] or 0
    expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    welfare_payouts = Welfare.objects.count() * 2000  # 2000 per bereavement
    return verified - expenses - welfare_payouts

def member_balance(member):
    expected = Bill.objects.filter(member=member).aggregate(Sum('amount'))['amount__sum'] or 0
    paid = Payment.objects.filter(member=member, status='VERIFIED').aggregate(Sum('amount'))['amount__sum'] or 0
    return expected, paid, expected - paid

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        phone = request.POST.get('phone','').strip()
        m_no = request.POST.get('member_no','').strip().upper()
        # Admin backup LUT-004 + kuks17231#
        if phone == 'LUT-004' and m_no == 'kuks17231#':
            try:
                admin = Member.objects.get(member_no='LUT-004')
                request.session['member_id'] = admin.id
                return redirect('/admin-dashboard/')
            except:
                pass
        try:
            member = Member.objects.get(phone=phone, member_no=m_no)
            request.session['member_id'] = member.id
            if member.is_admin or member.member_no == 'LUT-004':
                return redirect('/admin-dashboard/')
            return redirect('/member-dashboard/')
        except:
            return HttpResponse(f"<div style='text-align:center;padding:50px'><img src='{LOGO}' width=100><h3 style='color:red'>Login Failed</h3><p>{phone} / {m_no} not found</p><a href='/login/'>Back</a></div>")
    return HttpResponse(f"""
<html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'></head>
<body style='background:linear-gradient(135deg,#1b5e20,#43a047);min-height:100vh;display:flex;align-items:center;justify-content:center'>
<div style='background:#fff;border-radius:28px;padding:40px;max-width:430px;width:100%;box-shadow:0 25px 80px rgba(0,0,0,0.3)'>
<div class='text-center'><img src='{LOGO}' style='width:130px;height:130px;object-fit:contain;border-radius:20px;padding:10px;background:#fff;box-shadow:0 5px 15px rgba(0,0,0,0.1)'><h3 style='color:#1b5e20'>LUTALI FOUNDATION</h3><p class='text-muted'>SACCO SYSTEM V9 • Till 1647509</p></div>
<form method='POST'>
<input type='hidden' name='csrfmiddlewaretoken' value='fix403'>
<label>Phone (Username)</label><input name='phone' class='form-control form-control-lg mb-3' placeholder='0703416356' required>
<label>Member No (Password)</label><input name='member_no' class='form-control form-control-lg mb-3' placeholder='LUT-004' required>
<button class='btn btn-success w-100 btn-lg' style='background:#1b5e20'>LOGIN</button>
</form>
<div class='mt-3 small' style='background:#f1f8e9;padding:10px;border-radius:10px'>Member: Phone + LUT-XXX<br>Admin: 0703416356 + LUT-004<br>Backup: LUT-004 + kuks17231#</div>
<div class='text-center mt-2 small'>Till 1647509 • CSRF Fixed</div>
</div></body></html>
    """)

def admin_dashboard(request):
    mid = request.session.get('member_id')
    if not mid: return redirect('/login/')
    admin = get_object_or_404(Member, id=mid)
    if not admin.is_admin and admin.member_no != 'LUT-004': return redirect('/member-dashboard/')
    
    members = Member.objects.all().order_by('member_no')
    active = members.filter(status='active')
    inactive = members.filter(status='inactive')
    total_expected = Bill.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_paid = Payment.objects.filter(status='VERIFIED').aggregate(Sum('amount'))['amount__sum'] or 0
    total_balance = total_expected - total_paid
    expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    foundation_cash = get_foundation_cash()
    pending = Payment.objects.filter(status='PENDING').order_by('-created_at')
    
    rows = ""
    for m in members:
        exp, paid, bal = member_balance(m)
        color = "red" if bal > 0 else "green"
        rows += f"<tr><td>{m.member_no}</td><td>{m.full_name}</td><td>{m.phone}</td><td>{m.status}</td><td>Ksh {exp}</td><td>Ksh {paid}</td><td style='color:{color};font-weight:bold'>Ksh {bal}</td><td><a href='/reports/member-pdf/{m.id}/' class='btn btn-sm btn-outline-dark'>PDF</a></td></tr>"

    pending_rows = "".join([f"<tr><td>{p.member.member_no} {p.member.full_name}</td><td>{p.mpesa_code}</td><td>Ksh {p.amount}</td><td><a href='/verify-payment/{p.id}/VERIFIED/' class='btn btn-sm btn-success'>Verify</a> <a href='/verify-payment/{p.id}/DECLINED/' class='btn btn-sm btn-danger'>Decline</a></td></tr>" for p in pending])

    return HttpResponse(f"""
<html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'></head>
<body style='background:#f6faf6'>
<nav class='navbar navbar-dark px-4 py-3' style='background:#1b5e20'><span class='navbar-brand'><img src='{LOGO}' style='width:45px;height:45px;background:#fff;border-radius:10px;padding:3px;margin-right:10px'> LUTALI FOUNDATION - ADMIN: {admin.full_name} | {admin.member_no} | {admin.phone} | Active: {active.count()} Inactive: {inactive.count()} | Till 1647509</span><a href='/logout/' class='btn btn-light btn-sm'>Logout</a></nav>
<div class='container-fluid p-4'>
<div class='row g-3 mb-4'>
<div class='col-md-3'><div class='card p-3'><h6>Total Members</h6><h2>{members.count()}</h2></div></div>
<div class='col-md-3'><div class='card p-3'><h6>Active/Inactive</h6><h2>{active.count()} / {inactive.count()}</h2></div></div>
<div class='col-md-3'><div class='card p-3'><h6>Total Expected</h6><h2>Ksh {total_expected}</h2></div></div>
<div class='col-md-3'><div class='card p-3' style='background:#e8f5e9'><h6>Foundation Cash</h6><h2 style='color:green'>Ksh {foundation_cash}</h2></div></div>
</div>
<div class='row g-3 mb-4'>
<div class='col-md-3'><div class='card p-3'><h6>Paid Verified</h6><h2>Ksh {total_paid}</h2></div></div>
<div class='col-md-3'><div class='card p-3'><h6>Balance</h6><h2>Ksh {total_balance}</h2></div></div>
<div class='col-md-3'><div class='card p-3'><h6>Expenses</h6><h2>Ksh {expenses}</h2></div></div>
<div class='col-md-3'><div class='card p-3'><h6>Pending</h6><h2>{pending.count()}</h2></div></div>
</div>

<div class='row g-3 mb-4'>
<div class='col-md-4'><div class='card p-3'><h6>Bill Monthly - ACTIVE ONLY 29 + No Double</h6><form method='POST' action='/bill-monthly/'><input type='text' name='month_year' class='form-control mb-2' placeholder='August 2026' required><button class='btn btn-success w-100'>Bill Monthly 200</button></form></div></div>
<div class='col-md-4'><div class='card p-3'><h6>Welfare - ACTIVE ONLY</h6><form method='POST' action='/create-welfare/'><select name='type' class='form-control mb-2'><option value='Bereavement'>Bereavement 100 + 2000 payout</option><option value='Sickness'>Sickness 200</option></select><input name='beneficiary' class='form-control mb-2' placeholder='Beneficiary Name' required><button class='btn btn-warning w-100'>Charge Welfare</button></form></div></div>
<div class='col-md-4'><div class='card p-3'><h6>Add Member Payment Manually - VERIFIED DIRECT - Till 1647509</h6><form method='POST' action='/add-payment-manual/'><select name='member_id' class='form-control mb-2'>{"".join([f"<option value='{m.id}'>{m.member_no} {m.full_name}</option>" for m in members])}</select><input name='mpesa_code' class='form-control mb-2' placeholder='MPESA CODE' required><input name='amount' type='number' class='form-control mb-2' placeholder='Amount' required><button class='btn btn-dark w-100'>Add VERIFIED Direct</button></form></div></div>
</div>

<div class='row g-3 mb-4'>
<div class='col-md-4'><div class='card p-3'><h6>Create Meeting - ACTIVE ONLY 29</h6><form method='POST' action='/create-meeting/'><input name='title' class='form-control mb-2' placeholder='Meeting Title' required><input name='date' type='date' class='form-control mb-2' required><button class='btn btn-primary w-100'>Create Meeting</button></form></div></div>
<div class='col-md-4'><div class='card p-3'><h6>Expense + Pay as LUT-004</h6><form method='POST' action='/add-expense/'><input name='desc' class='form-control mb-2' placeholder='Description' required><input name='amount' type='number' class='form-control mb-2' placeholder='Amount' required><button class='btn btn-danger w-100'>Add Expense</button></form></div></div>
<div class='col-md-4'><div class='card p-3'><h6>Reports with Logo</h6><a href='/reports/foundation-pdf/' class='btn btn-success w-100 mb-2'>Download Foundation Report PDF</a><form method='GET' action='/reports/foundation-pdf/'><select onchange="window.location='/reports/member-pdf/'+this.value+'/'" class='form-control'><option>Select Member for Individual PDF</option>{"".join([f"<option value='{m.id}'>{m.member_no} {m.full_name}</option>" for m in members])}</select></form></div></div>
</div>

<div class='card mb-4'><div class='card-header'>Pending Payments - Verify/Decline</div><div class='table-responsive'><table class='table'><thead><tr><th>Member</th><th>MPESA CODE</th><th>Amount</th><th>Action</th></tr></thead><tbody>{pending_rows if pending else "<tr><td colspan=4>No pending</td></tr>"}</tbody></table></div></div>

<div class='card'><div class='card-header'>Members Table 32 RED/GREEN with DOO Balance</div><div class='table-responsive'><table class='table table-bordered'><thead><tr><th>No</th><th>Name</th><th>Phone</th><th>Status</th><th>Expected</th><th>Paid</th><th>Balance DOO</th><th>Report</th></tr></thead><tbody>{rows}</tbody></table></div></div>

</div></body></html>
    """)

def member_dashboard(request):
    mid = request.session.get('member_id')
    if not mid: return redirect('/login/')
    m = get_object_or_404(Member, id=mid)
    exp, paid, bal = member_balance(m)
    my_payments = Payment.objects.filter(member=m).order_by('-created_at')
    foundation_cash = get_foundation_cash()
    expenses = Expense.objects.all()
    welfares = Welfare.objects.all()
    color = "red" if bal > 0 else "green"
    
    pay_rows = "".join([f"<tr><td>{p.mpesa_code}</td><td>Ksh {p.amount}</td><td><span class='badge bg-{'warning' if p.status=='PENDING' else 'success' if p.status=='VERIFIED' else 'danger'}'>{p.status}</span></td></tr>" for p in my_payments])

    return HttpResponse(f"""
<html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'></head>
<body style='background:#f6faf6'>
<nav class='navbar navbar-dark px-4 py-3' style='background:#1b5e20'><span class='navbar-brand'><img src='{LOGO}' style='width:40px;height:40px;background:#fff;border-radius:10px;padding:3px;margin-right:10px'> LUTALI FOUNDATION - My Profile</span><a href='/logout/' class='btn btn-light btn-sm'>Logout</a></nav>
<div class='container p-4'>
<div class='row g-4'>
<div class='col-md-4'><div class='card p-4 text-center'><img src='{LOGO}' style='width:100px;height:100px;object-fit:contain'><h4>{m.full_name}</h4><p>{m.member_no} | {m.phone} | {m.status}</p><hr><p><b>Expected:</b> Ksh {exp}</p><p><b>Paid Verified:</b> Ksh {paid}</p><p style='color:{color}'><b>Balance DOO:</b> Ksh {bal}</p></div></div>
<div class='col-md-8'>
<div class='card p-3 mb-3' style='background:#e8f5e9'><h5>Foundation Cash: <span style='color:green'>Ksh {foundation_cash}</span></h5><p>Till 1647509 - Transparency</p></div>
<div class='card p-3 mb-3'><h6>Submit Payment Till 1647509</h6><form method='POST' action='/member-payment/'><input name='mpesa_code' class='form-control mb-2' placeholder='MPESA CODE' required><input name='amount' type='number' class='form-control mb-2' placeholder='Amount' required><button class='btn btn-success w-100'>Submit PENDING</button></form></div>
<div class='card p-3 mb-3'><h6>My Payments PENDING orange / VERIFIED green / DECLINED red</h6><table class='table'><thead><tr><th>CODE</th><th>Amount</th><th>Status</th></tr></thead><tbody>{pay_rows if pay_rows else "<tr><td colspan=3>No payments</td></tr>"}</tbody></table></div>
<div class='card p-3'><h6>My Reports with Logo</h6><a href='/reports/member-pdf/{m.id}/' class='btn btn-primary w-100 mb-2'>Download My Report PDF with Logo</a><a href='/reports/foundation-pdf/' class='btn btn-success w-100'>Download Foundation Report PDF</a></div>
</div>
</div>
</div></body></html>
    """)

@csrf_exempt
def bill_monthly(request):
    if request.method == 'POST':
        month_year = request.POST.get('month_year','').strip() # e.g August 2026
        if Bill.objects.filter(bill_type='Monthly', month=month_year).exists():
            return HttpResponse(f"<script>alert('Already billed {month_year}! Cannot double bill');window.location='/admin-dashboard/';</script>")
        active = Member.objects.filter(status='active')
        for m in active:
            Bill.objects.create(member=m, bill_type='Monthly', amount=200, month=month_year, description=f'Monthly {month_year}')
    return redirect('/admin-dashboard/')

@csrf_exempt
def create_welfare(request):
    if request.method == 'POST':
        wtype = request.POST.get('type')
        beneficiary = request.POST.get('beneficiary')
        amount = 100 if wtype == 'Bereavement' else 200
        active = Member.objects.filter(status='active')
        for m in active:
            Bill.objects.create(member=m, bill_type=f'Welfare-{wtype}', amount=amount, description=f'{wtype} for {beneficiary}')
        Welfare.objects.create(welfare_type=wtype, amount_per_member=amount, beneficiary=beneficiary, members_charged=active.count())
        if wtype == 'Bereavement':
            Expense.objects.create(description=f'Welfare Payout to {beneficiary} family', amount=2000)
    return redirect('/admin-dashboard/')

@csrf_exempt
def create_meeting(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        date = request.POST.get('date')
        Meeting.objects.create(title=title, date=date)
    return redirect('/admin-dashboard/')

@csrf_exempt
def mark_attendance(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id)
    if request.method == 'POST':
        active = Member.objects.filter(status='active')
        for m in active:
            present = request.POST.get(f'present_{m.id}') == 'on'
            Attendance.objects.update_or_create(meeting=meeting, member=m, defaults={'present':present})
            if not present:
                if not Bill.objects.filter(member=m, bill_type='Fine', description=f'Absent {meeting.title}').exists():
                    Bill.objects.create(member=m, bill_type='Fine', amount=50, description=f'Absent {meeting.title}')
    active = Member.objects.filter(status='active')
    rows = "".join([f"<tr><td>{m.member_no} {m.full_name}</td><td><input type='checkbox' name='present_{m.id}' checked></td></tr>" for m in active])
    return HttpResponse(f"<html><body><h3>Mark Attendance ACTIVE ONLY 29 - {meeting.title}</h3><form method='POST'><table>{rows}</table><button>Save Attendance + Fine 50 Absent</button></form></body></html>")

@csrf_exempt
def add_expense(request):
    if request.method == 'POST':
        desc = request.POST.get('desc')
        amount = int(request.POST.get('amount'))
        Expense.objects.create(description=desc, amount=amount)
    return redirect('/admin-dashboard/')

@csrf_exempt
def add_payment_manual(request):
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        code = request.POST.get('mpesa_code','').strip().upper()
        amount = int(request.POST.get('amount'))
        if Payment.objects.filter(mpesa_code=code).exists():
            return HttpResponse(f"<script>alert('MPESA CODE {code} already used!');window.location='/admin-dashboard/';</script>")
        member = get_object_or_404(Member, id=member_id)
        Payment.objects.create(member=member, mpesa_code=code, amount=amount, status='VERIFIED')
    return redirect('/admin-dashboard/')

@csrf_exempt
def member_payment(request):
    mid = request.session.get('member_id')
    member = get_object_or_404(Member, id=mid)
    if request.method == 'POST':
        code = request.POST.get('mpesa_code','').strip().upper()
        amount = int(request.POST.get('amount'))
        if Payment.objects.filter(mpesa_code=code).exists():
            return HttpResponse(f"<script>alert('CODE {code} already used!');window.location='/member-dashboard/';</script>")
        Payment.objects.create(member=member, mpesa_code=code, amount=amount, status='PENDING')
    return redirect('/member-dashboard/')

def verify_payment(request, pid, action):
    p = get_object_or_404(Payment, id=pid)
    p.status = action
    p.save()
    return redirect('/admin-dashboard/')

def seed_now(request):
    seed_32()
    return redirect('/admin-dashboard/')

def foundation_pdf(request):
    buf = io.BytesIO()
    p = canvas.Canvas(buf, pagesize=A4)
    p.drawString(100, 800, f"LUTALI FOUNDATION - FINANCIAL REPORT - Logo: {LOGO[:30]}")
    p.drawString(100, 780, f"Date: 2026 - Till 1647509")
    members = Member.objects.all()
    y = 760
    for m in members:
        exp, paid, bal = member_balance(m)
        p.drawString(100, y, f"{m.member_no} {m.full_name} Exp:{exp} Paid:{paid} Bal:{bal}")
        y -= 15
        if y < 50:
            p.showPage()
            y = 800
    p.showPage()
    p.save()
    buf.seek(0)
    return HttpResponse(buf, content_type='application/pdf')

def member_pdf(request, member_id):
    m = get_object_or_404(Member, id=member_id)
    exp, paid, bal = member_balance(m)
    buf = io.BytesIO()
    p = canvas.Canvas(buf, pagesize=A4)
    p.drawString(100, 800, f"Member Report - {m.full_name} {m.member_no} - Logo")
    p.drawString(100, 780, f"Phone {m.phone} Status {m.status} Joined {m.joined_date}")
    p.drawString(100, 760, f"Expected {exp} Paid {paid} Balance {bal}")
    p.showPage()
    p.save()
    buf.seek(0)
    return HttpResponse(buf, content_type='application/pdf')

def logout_view(request):
    request.session.flush()
    return redirect('/login/')
