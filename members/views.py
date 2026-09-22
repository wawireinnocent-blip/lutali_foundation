from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from.models import Member

@csrf_exempt
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
            return HttpResponse("<script>alert('Phone au Member No sio sahihi!');window.location='/member-login/';</script>")
    return HttpResponse("""
    <!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>
    <style>body{background:#eef2f7;display:flex;align-items:center;justify-content:center;min-height:100vh}
   .login-card{width:100%;max-width:420px;background:#fff;border-radius:20px;padding:35px;box-shadow:0 15px 40px rgba(0,0,0,0.1)}</style></head><body>
    <div class='login-card text-center'>
    <div style='width:80px;height:80px;background:linear-gradient(135deg,#1a3a5f,#2e7d32);color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:bold;margin:0 auto 10px'>LF</div>
    <h4 class='fw-bold'>Lutali Foundation</h4><p class='text-muted'>Community Welfare Group</p><p class='text-muted small mb-4'>Members Portal</p>
    <form method='POST' class='text-start'>
    <label class='fw-bold'>Phone Number (Username)</label><input name='phone' class='form-control form-control-lg mb-3' placeholder='07XXXXXXXX' required>
    <label class='fw-bold'>Member Number (Password)</label><input name='member_no' class='form-control form-control-lg mb-3' placeholder='LUT-001' required>
    <button class='btn btn-dark w-100 btn-lg mt-2'>LOGIN</button></form>
    <div class='mt-3 small text-muted'>Test: 0792967633 / LUT-002</div></div></body></html>
    """)

def admin_dashboard(request):
    members = Member.objects.all().order_by('member_no')
    count = members.count()
    rows = "".join([f"<tr><td><span class='badge bg-dark'>{m.member_no}</span></td><td class='fw-bold'>{m.full_name}</td><td>{m.phone}</td><td><span class='badge bg-success'>{m.status}</span></td><td><a href='/delete-member/{m.id}/' class='btn btn-sm btn-outline-danger' onclick=\"return confirm('Delete?')\">Delete</a></td></tr>" for m in members])
    if count==0: rows="<tr><td colspan=5 class='text-center py-4'><a href='/import-now/' class='btn btn-warning'>IMPORT 32 MEMBERS</a></td></tr>"
    return HttpResponse(f"""
    <!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'></head><body style='background:#f4f6f9'>
    <nav class='navbar navbar-dark bg-dark px-4'><span class='navbar-brand fw-bold'><span style='background:#fff;color:#000;border-radius:50%;padding:5px 10px;margin-right:8px'>LF</span> LUTALI FOUNDATION</span><div><a href='/reports/' class='btn btn-sm btn-warning me-2'>Reports</a><a href='/logout/' class='btn btn-sm btn-light'>Logout</a></div></nav>
    <div class='container mt-4'><div class='row g-3 mb-4'><div class='col-md-4'><div class='card p-3 shadow-sm'><h6 class='text-muted'>Total Members</h6><h2>{count}</h2></div></div><div class='col-md-4'><div class='card p-3 shadow-sm'><h6 class='text-muted'>Active</h6><h2 class='text-success'>{count}</h2></div></div><div class='col-md-4'><div class='card p-3 shadow-sm'><h6 class='text-muted'>Status</h6><h2 class='text-primary'>LIVE</h2></div></div></div>
    <div class='card shadow-sm'><div class='card-header bg-white d-flex justify-content-between'><h5>Members Register</h5><a href='/reports/' class='btn btn-sm btn-dark'>Professional Report</a></div><div class='table-responsive'><table class='table table-hover mb-0'><thead class='table-light'><tr><th>No</th><th>Name</th><th>Phone</th><th>Status</th><th>Action</th></tr></thead><tbody>{rows}</tbody></table></div></div></div></body></html>
    """)

def member_dashboard(request):
    mid=request.session.get('member_id')
    if not mid: return redirect('/member-login/')
    m=get_object_or_404(Member, id=mid)
    return HttpResponse(f"""
    <!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'></head><body style='background:#f4f6f9'>
    <nav class='navbar navbar-dark bg-dark px-4'><span class='navbar-brand fw-bold'>LF - LUTALI FOUNDATION</span><a href='/logout/' class='btn btn-sm btn-light'>Logout</a></nav>
    <div class='container mt-4'><div class='row'><div class='col-md-4'><div class='card shadow-sm p-4 text-center'><div style='width:80px;height:80px;background:#1a3a5f;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:32px;margin:0 auto'>{m.full_name[0]}</div><h4 class='mt-3'>{m.full_name}</h4><p class='text-muted'>{m.member_no}</p><span class='badge bg-success'>{m.status}</span><hr><p class='text-start'><b>Phone:</b> {m.phone}</p><p class='text-start'><b>Member No:</b> {m.member_no}</p></div></div>
    <div class='col-md-8'><div class='card shadow-sm p-4'><h5>Karibu {m.full_name.split()[0]}!</h5><p>Welcome to Lutali Foundation Members Portal</p><div class='alert alert-success'>Account yako iko Active na iko salama.</div></div></div></div></div></body></html>
    """)

def reports(request):
    members=Member.objects.all().order_by('member_no')
    rows="".join([f"<tr><td>{i+1}</td><td>{m.member_no}</td><td>{m.full_name}</td><td>{m.phone}</td><td>{m.status}</td><td>____________</td></tr>" for i,m in enumerate(members)])
    return HttpResponse(f"""
    <!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
    <link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css' rel='stylesheet'>
    <style>@media print{{.no-print{{display:none}}}}</style></head><body style='background:#fff'>
    <div class='container mt-4'><div class='text-center mb-4'><div style='width:80px;height:80px;background:#1a3a5f;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:28px;font-weight:bold;margin:0 auto'>LF</div><h2 class='fw-bold mt-2'>LUTALI FOUNDATION</h2><p class='text-muted'>Community Welfare Group - Kakamega</p><h5 class='fw-bold'>OFFICIAL MEMBERS REGISTER REPORT</h5><p>Date: 22/09/2026 | Total Members: {members.count()}</p><hr></div>
    <table class='table table-bordered'><thead class='table-dark'><tr><th>#</th><th>Member No</th><th>Full Name</th><th>Phone Number</th><th>Status</th><th>Signature</th></tr></thead><tbody>{rows}</tbody></table>
    <div class='row mt-5'><div class='col-6'><p>_________________________<br><b>Chairman Signature</b><br>ISAAC FRED (LUT-001)</p></div><div class='col-6 text-end'><p>_________________________<br><b>Secretary Signature</b><br>Date: 22/09/2026</p></div></div>
    <div class='text-center mt-4 no-print'><button onclick='window.print()' class='btn btn-dark btn-lg'>Print / Save PDF</button> <a href='/admin-dashboard/' class='btn btn-outline-dark btn-lg'>Back to Dashboard</a></div></div></body></html>
    """)

def member_logout(request):
    request.session.flush()
    return redirect('/member-login/')

def delete_member(request, member_id):
    try: Member.objects.get(id=member_id).delete()
    except: pass
    return redirect('/admin-dashboard/')

def import_now(request):
    if Member.objects.count() >= 32: return redirect('/admin-dashboard/')
    if Member.objects.count()>0: Member.objects.all().delete()
    data = [('LUT-001','ISAAC FRED','0768760386'),('LUT-002','Esther Luchivia','0792967633'),('LUT-003','Ajella Mulari','0759531836'),('LUT-004','INNOCENT WAWIRE','0703416356'),('LUT-005','Laban Fula','0111410769'),('LUT-006','KenPeter Muchika','0768075466'),('LUT-007','Melvin Barasa','0797969333'),('LUT-008','Mildred Lumbasi','0707397500'),('LUT-009','Leah Juma','0701434949'),('LUT-010','Yvonne Kharinda','0759221476'),('LUT-011','Christine Zipporah','0742023615'),('LUT-012','Alex Koikoi','0706313051'),('LUT-013','Joshua Sindani','0791279560'),('LUT-014','Emmanuel Sunguti','0727994764'),('LUT-015','Cedrick Chivuyi','0705890849'),('LUT-016','Mildred Nekesa','0713364628'),('LUT-017','Burntone Kulova','0700602172'),('LUT-018','Isaiah Wete','0758795051'),('LUT-019','Austin Mando','0715244622'),('LUT-020','Ali Kibaya','0798911493'),('LUT-021','Philemon Tom','0748343436'),('LUT-022','Nicole Nakhumicha','0796610007'),('LUT-023','Mercyline Mutenyo','0707828521'),('LUT-024','Salome Salim','0795983430'),('LUT-025','Leah Salim','0729010826'),('LUT-026','John Museve','0798709891'),('LUT-027','Esther Kharinda','0707277721'),('LUT-028','Gloria Imbiakha','0743166089'),('LUT-029','Daniel Solomon','0758570045'),('LUT-030','Elizabeth Muhonja','0795313500'),('LUT-031','Gelda Weyala','0712694179'),('LUT-032','Yvonne Mwenesi','0787849794'),]
    for no,name,phone in data: Member.objects.create(member_no=no, full_name=name, phone=phone, status="Active")
    return redirect('/admin-dashboard/')
