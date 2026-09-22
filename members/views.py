from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from .models import Member

def home(request):
    return redirect('/member-login/')

def member_login(request):
    if request.method == 'POST':
        phone = request.POST.get('phone','').strip()
        member_no = request.POST.get('member_no','').strip().upper()
        try:
            member = Member.objects.get(phone=phone, member_no=member_no)
            request.session['member_id'] = member.id
            request.session['member_no'] = member.member_no
            if member.member_no == 'LUT-001':
                return redirect('/admin-dashboard/')
            return redirect('/member-dashboard/')
        except:
            return HttpResponse("<html><body style='font-family:Arial;padding:20px;text-align:center'><h3 style='color:red'>Phone au Member Number sio sahihi!</h3><p>Phone: 0792967633 , Password: LUT-002</p><a href='/member-login/'>Try Again</a></body></html>")
    return HttpResponse("""
    <html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
    <style>body{font-family:Arial;background:#f0f2f5;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}
    .box{background:white;padding:30px;border-radius:10px;box-shadow:0 0 10px #ccc;width:90%;max-width:350px}
    input{width:100%;padding:12px;margin:8px 0;border:1px solid #ccc;border-radius:5px}
    button{width:100%;padding:12px;background:#2c3e50;color:white;border:none;border-radius:5px;margin-top:10px;font-weight:bold}
    </style></head><body>
    <div class='box'>
    <h2 style='text-align:center'>Lutali Foundation</h2>
    <p style='text-align:center;color:gray'>Member Login</p>
    <form method='POST'>
    <label><b>Phone Number (Username)</b></label>
    <input name='phone' placeholder='07XXXXXXXX' required>
    <label><b>Member Number (Password)</b></label>
    <input name='member_no' placeholder='LUT-001' required>
    <button type='submit'>LOGIN</button>
    </form>
    <br><div style='background:#eef;padding:10px;border-radius:5px;font-size:13px'>
    <b>Mfano:</b><br>Username: 0792967633<br>Password: LUT-002
    </div>
    </div></body></html>
    """)

def member_dashboard(request):
    member_id = request.session.get('member_id')
    if not member_id:
        return redirect('/member-login/')
    member = get_object_or_404(Member, id=member_id)
    return HttpResponse(f"""
    <html><head><meta name='viewport' content='width=device-width, initial-scale=1'>
    <style>body{{font-family:Arial;padding:20px;background:#f5f5f5}} .card{{background:white;padding:20px;border-radius:10px}}</style></head><body>
    <div class='card'>
    <h2>Karibu, {member.full_name}!</h2>
    <p><b>Member No:</b> {member.member_no}</p>
    <p><b>Phone:</b> {member.phone}</p>
    <p><b>Status:</b> {member.status}</p>
    <hr><p>Foundation: Lutali Foundation</p>
    <br><a href='/logout/' style='background:red;color:white;padding:10px;text-decoration:none;border-radius:5px'>Logout</a>
    </div></body></html>
    """)

def member_logout(request):
    request.session.flush()
    return redirect('/member-login/')

def admin_dashboard(request):
    members = Member.objects.all().order_by('member_no')
    count = members.count()
    rows = ""
    for m in members:
        rows += f"<tr><td>{m.member_no}</td><td>{m.full_name}</td><td>{m.phone}</td><td>{m.status}</td><td><a href='/delete-member/{m.id}/'>Delete</a></td></tr>"
    if count == 0:
        rows = "<tr><td colspan=5 style='text-align:center'><a href='/import-now/'>CLICK TO IMPORT 32</a></td></tr>"
    return HttpResponse(f"<html><body style='font-family:Arial;padding:20px'><h1>Admin - {count} Members</h1><a href='/member-login/'>Member Login</a> | <a href='/logout/'>Logout</a><br><br><table border=1 cellpadding=10 width=100%><tr><th>No</th><th>Name</th><th>Phone</th><th>Status</th><th>Action</th></tr>{rows}</table></body></html>")

def add_member(request):
    return redirect('/admin-dashboard/')

def edit_member(request, member_id):
    return redirect('/admin-dashboard/')

def delete_member(request, member_id):
    try:
        Member.objects.get(id=member_id).delete()
    except:
        pass
    return redirect('/admin-dashboard/')

def import_now(request):
    if Member.objects.count() >= 32:
        return redirect('/admin-dashboard/')
    Member.objects.all().delete()
    data = [('LUT-001','ISAAC FRED','0768760386'),('LUT-002','Esther Luchivia','0792967633'),('LUT-003','Ajella Mulari','0759531836'),('LUT-004','INNOCENT WAWIRE','0703416356'),('LUT-005','Laban Fula','0111410769'),('LUT-006','KenPeter Muchika','0768075466'),('LUT-007','Melvin  Barasa','0797969333'),('LUT-008','Mildred Lumbasi','0707397500'),('LUT-009','Leah Juma','0701434949'),('LUT-010','Yvonne Kharinda','0759221476'),('LUT-011','Christine Zipporah','0742023615'),('LUT-012','Alex Koikoi','0706313051'),('LUT-013','Joshua Sindani','0791279560'),('LUT-014','Emmanuel Sunguti','0727994764'),('LUT-015','Cedrick Chivuyi','0705890849'),('LUT-016','Mildred Nekesa','0713364628'),('LUT-017','Burntone Kulova','0700602172'),('LUT-018','Isaiah Wete','0758795051'),('LUT-019','Austin Mando','0715244622'),('LUT-020','Ali Kibaya','0798911493'),('LUT-021','Philemon Tom','0748343436'),('LUT-022','Nicole Nakhumicha','0796610007'),('LUT-023','Mercyline Mutenyo','0707828521'),('LUT-024','Salome Salim','0795983430'),('LUT-025','Leah Salim','0729010826'),('LUT-026','John Museve','0798709891'),('LUT-027','Esther Kharinda','0707277721'),('LUT-028','Gloria Imbiakha','0743166089'),('LUT-029','Daniel Solomon','0758570045'),('LUT-030','Elizabeth Muhonja','0795313500'),('LUT-031','Gelda Weyala','0712694179'),('LUT-032','Yvonne Mwenesi','0787849794'),]
    for no,name,phone in data:
        Member.objects.create(member_no=no, full_name=name, phone=phone, status="Active")
    return redirect('/admin-dashboard/')
