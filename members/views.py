from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Member

def home(request):
    return redirect('/admin-dashboard/')

def admin_dashboard(request):
    members = Member.objects.all().order_by('member_no')
    count = members.count()
    rows = ""
    for m in members:
        rows += f"<tr><td>{m.member_no}</td><td>{m.full_name}</td><td>{m.phone}</td><td>{m.status}</td><td><a href='/edit-member/{m.id}/' style='color:blue'>Edit</a> | <a href='/delete-member/{m.id}/' style='color:red'>Delete</a></td></tr>"
    if count == 0:
        rows = "<tr><td colspan='5' style='text-align:center;padding:20px;color:red'><b>DATABASE EMPTY! <a href='/import-now/' style='background:red;color:white;padding:10px'>CLICK HERE TO IMPORT YOUR 32 REAL MEMBERS</a></b></td></tr>"
    html = f"""
    <html><head><title>Lutali Admin</title>
    <style>body{{font-family:Arial;padding:20px}}table{{width:100%;border-collapse:collapse}}th,td{{border:1px solid #ccc;padding:10px}}th{{background:#2c3e50;color:#fff}}</style>
    </head><body>
    <h1>Lutali Foundation - Members ({count})</h1>
    <a href='/add-member/' style='background:green;color:white;padding:10px 15px;border-radius:5px;text-decoration:none'>+ ADD MEMBER</a> | <a href='/import-now/' style='background:orange;color:white;padding:10px 15px;border-radius:5px;text-decoration:none'>IMPORT 32</a>
    <br><br><table><tr><th>Member No</th><th>Full Name</th><th>Phone</th><th>Status</th><th>Action</th></tr>{rows}</table>
    </body></html>
    """
    return HttpResponse(html)

@csrf_exempt
def add_member(request):
    if request.method == 'POST':
        Member.objects.create(member_no=request.POST.get('member_no'), full_name=request.POST.get('full_name'), phone=request.POST.get('phone'), status=request.POST.get('status','Active'))
        return redirect('/admin-dashboard/')
    return HttpResponse("<h2>Add Member</h2><form method='POST'>No: <input name='member_no' required><br><br>Name: <input name='full_name' required><br><br>Phone: <input name='phone' required><br><br>Status: <input name='status' value='Active'><br><br><button type='submit'>SAVE</button></form><br><a href='/admin-dashboard/'>Back</a>")

@csrf_exempt
def edit_member(request, member_id):
    m = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        m.member_no = request.POST.get('member_no'); m.full_name = request.POST.get('full_name'); m.phone = request.POST.get('phone'); m.status = request.POST.get('status'); m.save()
        return redirect('/admin-dashboard/')
    return HttpResponse(f"<h2>Edit {m.full_name}</h2><form method='POST'>No: <input name='member_no' value='{m.member_no}' required><br><br>Name: <input name='full_name' value='{m.full_name}' required><br><br>Phone: <input name='phone' value='{m.phone}' required><br><br>Status: <input name='status' value='{m.status}'><br><br><button type='submit'>UPDATE</button></form><br><a href='/admin-dashboard/'>Back</a>")

def delete_member(request, member_id):
    m = get_object_or_404(Member, id=member_id); m.delete(); return redirect('/admin-dashboard/')

def import_now(request):
    Member.objects.all().delete()
    data = [
        ('LUT-001','ISAAC FRED','0768760386'),
        ('LUT-002','Esther Luchivia','0792967633'),
        ('LUT-003','Ajella Mulari','0759531836'),
        ('LUT-004','INNOCENT WAWIRE','0703416356'),
        ('LUT-005','Laban Fula','0111410769'),
        ('LUT-006','KenPeter Muchika','0768075466'),
        ('LUT-007','Melvin  Barasa','0797969333'),
        ('LUT-008','Mildred Lumbasi','0707397500'),
        ('LUT-009','Leah Juma','0701434949'),
        ('LUT-010','Yvonne Kharinda','0759221476'),
        ('LUT-011','Christine Zipporah','0742023615'),
        ('LUT-012','Alex Koikoi','0706313051'),
        ('LUT-013','Joshua Sindani','0791279560'),
        ('LUT-014','Emmanuel Sunguti','0727994764'),
        ('LUT-015','Cedrick Chivuyi','0705890849'),
        ('LUT-016','Mildred Nekesa','0713364628'),
        ('LUT-017','Burntone Kulova','0700602172'),
        ('LUT-018','Isaiah Wete','0758795051'),
        ('LUT-019','Austin Mando','0715244622'),
        ('LUT-020','Ali Kibaya','0798911493'),
        ('LUT-021','Philemon Tom','0748343436'),
        ('LUT-022','Nicole Nakhumicha','0796610007'),
        ('LUT-023','Mercyline Mutenyo','0707828521'),
        ('LUT-024','Salome Salim','0795983430'),
        ('LUT-025','Leah Salim','0729010826'),
        ('LUT-026','John Museve','0798709891'),
        ('LUT-027','Esther Kharinda','0707277721'),
        ('LUT-028','Gloria Imbiakha','0743166089'),
        ('LUT-029','Daniel Solomon','0758570045'),
        ('LUT-030','Elizabeth Muhonja','0795313500'),
        ('LUT-031','Gelda Weyala','0712694179'),
        ('LUT-032','Yvonne Mwenesi','0787849794'),
    ]
    for no,name,phone in data:
        Member.objects.create(member_no=no, full_name=name, phone=phone, status="Active")
    return redirect('/admin-dashboard/')
