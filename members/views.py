from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from.models import Member

def member_login(request):
    if request.method == 'POST':
        phone = request.POST.get('phone','').strip()
        m_no = request.POST.get('member_no','').strip().upper()
        try:
            member = Member.objects.get(phone=phone, member_no=m_no)
            request.session['member_id'] = member.id
            request.session['role'] = 'admin' if member.member_no == 'LUT-001' else 'member'
            if member.member_no == 'LUT-001':
                return redirect('/admin-dashboard/')
            return redirect('/member-dashboard/')
        except:
            return HttpResponse("<script>alert('Phone au Member No sio sahihi! Jaribu Phone: 0792967633 na Password: LUT-002');window.location='/member-login/';</script>")

    return HttpResponse("""
    <!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>
    <style>body{background:#f4f6f9;display:flex;align-items:center;justify-content:center;min-height:100vh}
   .login-card{width:100%;max-width:420px;background:#fff;border-radius:15px;padding:35px;box-shadow:0 10px 30px rgba(0,0,0,0.1)}
   .logo{width:70px;height:70px;background:#1a3a5f;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:bold;margin:0 auto 15px}</style>
    </head><body>
    <div class='login-card'>
    <div class='logo'>LF</div>
    <h4 class='text-center fw-bold'>Lutali Foundation</h4>
    <p class='text-center text-muted mb-4'>Members Portal</p>
    <form method='POST'>
    <div class='mb-3'><label class='form-label fw-bold'>Phone Number</label><input type='text' name='phone' class='form-control form-control-lg' placeholder='e.g 0768760386' required></div>
    <div class='mb-3'><label class='form-label fw-bold'>Member Number</label><input type='text' name='member_no' class='form-control form-control-lg' placeholder='e.g LUT-001' required></div>
    <button class='btn btn-dark w-100 btn-lg mt-2'>LOGIN</button>
    </form>
    <div class='mt-4 p-3 bg-light rounded small'><b>Test Account:</b><br>Phone: 0792967633<br>Password: LUT-002</div>
    </div></body></html>
    """)

def admin_dashboard(request):
    if request.session.get('role')!= 'admin':
        # Ruhusu admin aingie bila session kama database iko empty kwa mara ya kwanza
        if Member.objects.count() > 0 and request.session.get('member_id') is None:
            return redirect('/member-login/')
    members = Member.objects.all().order_by('member_no')
    count = members.count()
    active = members.filter(status='ACTIVE').count()
    rows = "".join([f"<tr><td><span class='badge bg-dark'>{m.member_no}</span></td><td class='fw-bold'>{m.full_name}</td><td>{m.phone}</td><td><span class='badge bg-success'>{m.status}</span></td><td><a href='/delete-member/{m.id}/' class='btn btn-sm btn-outline-danger' onclick=\"return confirm('Futa {m.full_name}?')\">Delete</a></td></tr>" for m in members])
    if count == 0:
        rows = "<tr><td colspan=5 class='text-center py-4'><a href='/import-now/' class='btn btn-warning'>IMPORT 32 MEMBERS NOW</a></td></tr>"
    return HttpResponse(f"""
    <!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>
    </head><body style='background:#f4f6f9'>
    <nav class='navbar navbar-dark bg-dark px-4'><span class='navbar-brand fw-bold'>LUTALI FOUNDATION - ADMIN</span><a href='/logout/' class='btn btn-sm btn-light'>Logout</a></nav>
    <div class='container mt-4'>
    <div class='row g-3 mb-4'><div class='col-md-4'><div class='card p-3 shadow-sm'><h6 class='text-muted'>Total Members</h6><h2 class='fw-bold'>{count}</h2></div></div><div class='col-md-4'><div class='card p-3 shadow-sm'><h6 class='text-muted'>Active Members</h6><h2 class='fw-bold text-success'>{active}</h2></div></div><div class='col-md-4'><div class='card p-3 shadow-sm'><h6 class='text-muted'>System Status</h6><h2 class='fw-bold text-primary'>LIVE</h2></div></div></div>
    <div class='card shadow-sm'><div class='card-header bg-white d-flex justify-content-between align-items-center'><h5 class='mb-0'>All Members (32)</h5><a href='/member-login/' class='btn btn-sm btn-outline-dark'>Member Login Page</a></div>
    <div class='table-responsive'><table class='table table-hover mb-0'><thead class='table-light'><tr><th>Member No</th><th>Name</th><th>Phone</th><th>Status</th><th>Action</th></tr></thead><tbody>{rows}</tbody></table></div></div>
    </div></body></html>
    """)

def member_dashboard(request):
    mid = request.session.get('member_id')
    if not mid: return redirect('/member-login/')
    m = get_object_or_404(Member, id=mid)
    return HttpResponse(f"""
    <!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>
    </head><body style='background:#f4f6f9'>
    <nav class='navbar navbar-dark bg-dark px-4'><span class='navbar-brand fw-bold'>LUTALI FOUNDATION</span><a href='/logout/' class='btn btn-sm btn-light'>Logout</a></nav>
    <div class='container mt-4'>
    <div class='row'><div class='col-md-4'><div class='card shadow-sm p-4 text-center'><div style='width:80px;height:80px;background:#1a3a5f;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:32px;margin:0 auto'>{m.full_name[0]}</div><h4 class='mt-3 fw-bold'>{m.full_name}</h4><p class='text-muted'>{m.member_no}</p><span class='badge bg-success'>{m.status}</span><hr><p class='text-start mb-1'><b>Phone:</b> {m.phone}</p><p class='text-start mb-1'><b>Member No:</b> {m.member_no}</p><p class='text-start'><b>Joined:</b> Active Member</p></div></div>
    <div class='col-md-8'><div class='card shadow-sm p-4 mb-3'><h5>Karibu {m.full_name.split()[0]}!</h5><p class='text-muted'>Hii ni portal yako rasmi ya Lutali Foundation.</p><div class='alert alert-info'>Account yako iko active. Endelea kuchangia maendeleo ya foundation.</div></div>
    <div class='card shadow-sm p-4'><h6 class='fw-bold'>Foundation Info</h6><p class='small text-muted'>Lutali Foundation ni chama cha kusaidiana. Kwa maswali wasiliana na Admin: ISAAC FRED - 0768760386</p></div></div></div>
    </div></body></html>
    """)

def member_logout(request):
    request.session.flush()
    return redirect('/member-login/')

def delete_member(request, member_id):
    try: Member.objects.get(id=member_id).delete()
    except: pass
    return redirect('/admin-dashboard/')

def import_now(request):
    if Member.objects.count() >= 32:
        return redirect('/admin-dashboard/')
    if Member.objects.count() > 0:
        Member.objects.all().delete()
    data = [('LUT-001','ISAAC FRED','0768760386'),('LUT-002','Esther Luchivia','0792967633'),('LUT-003','Ajella Mulari','0759531836'),('LUT-004','INNOCENT WAWIRE','0703416356'),('LUT-005','Laban Fula','0111410769'),('LUT-006','KenPeter Muchika','0768075466'),('LUT-007','Melvin Barasa','0797969333'),('LUT-008','Mildred Lumbasi','0707397500'),('LUT-009','Leah Juma','0701434949'),('LUT-010','Yvonne Kharinda','0759221476'),('LUT-011','Christine Zipporah','0742023615'),('LUT-012','Alex Koikoi','0706313051'),('LUT-013','Joshua Sindani','0791279560'),('LUT-014','Emmanuel Sunguti','0727994764'),('LUT-015','Cedrick Chivuyi','0705890849'),('LUT-016','Mildred Nekesa','0713364628'),('LUT-017','Burntone Kulova','0700602172'),('LUT-018','Isaiah Wete','0758795051'),('LUT-019','Austin Mando','0715244622'),('LUT-020','Ali Kibaya','0798911493'),('LUT-021','Philemon Tom','0748343436'),('LUT-022','Nicole Nakhumicha','0796610007'),('LUT-023','Mercyline Mutenyo','0707828521'),('LUT-024','Salome Salim','0795983430'),('LUT-025','Leah Salim','0729010826'),('LUT-026','John Museve','0798709891'),('LUT-027','Esther Kharinda','0707277721'),('LUT-028','Gloria Imbiakha','0743166089'),('LUT-029','Daniel Solomon','0758570045'),('LUT-030','Elizabeth Muhonja','0795313500'),('LUT-031','Gelda Weyala','0712694179'),('LUT-032','Yvonne Mwenesi','0787849794'),]
    for no,name,phone in data: Member.objects.create(member_no=no, full_name=name, phone=phone, status="Active")
    return redirect('/admin-dashboard/')

def add_member(request): return redirect('/admin-dashboard/')
def edit_member(request, member_id): return redirect('/admin-dashboard/')
