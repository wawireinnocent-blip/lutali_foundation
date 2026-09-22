from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from .models import Member

def home(request):
    return redirect('/admin-dashboard/')

def admin_dashboard(request):
    members = Member.objects.all().order_by('member_no')
    
    # HTML ya moja kwa moja - hakuna haja ya template!
    html = """
    <html><head><title>Lutali Foundation - Admin</title>
    <style>
    body{font-family:Arial;padding:20px;background:#f5f5f5}
    table{width:100%;border-collapse:collapse;background:white}
    th,td{padding:10px;border:1px solid #ddd;text-align:left}
    th{background:#2c3e50;color:white}
    .btn{padding:5px 10px;text-decoration:none;border-radius:4px;margin:2px;display:inline-block}
    .btn-add{background:green;color:white} .btn-edit{background:blue;color:white} .btn-del{background:red;color:white}
    </style></head><body>
    <h1>Lutali Foundation - Members Dashboard</h1>
    <p>Total Members: """ + str(members.count()) + """</p>
    <a href='/add-member/' class='btn btn-add'>+ Add Member</a><br><br>
    <table><tr><th>No</th><th>Full Name</th><th>Phone</th><th>Status</th><th>Actions</th></tr>
    """
    for m in members:
        html += f"<tr><td>{m.member_no}</td><td>{m.full_name}</td><td>{m.phone}</td><td>{m.status}</td><td><a href='/edit-member/{m.id}/' class='btn btn-edit'>Edit</a> <a href='/delete-member/{m.id}/' class='btn btn-del'>Delete</a></td></tr>"
    
    if not members:
        html += "<tr><td colspan='5' style='text-align:center;color:red;'><b>Hakuna members bado - Enda Shell uandike: python import_members.py</b></td></tr>"
    
    html += "</table></body></html>"
    return HttpResponse(html)

def add_member(request):
    if request.method == 'POST':
        Member.objects.create(
            member_no=request.POST.get('member_no'),
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            status=request.POST.get('status','Active')
        )
        return redirect('/admin-dashboard/')
    return HttpResponse("""
    <h2>Add Member</h2>
    <form method='post'>""" + """<input type='hidden' name='csrfmiddlewaretoken' value=''>""" + """
    Member No: <input name='member_no' required><br><br>
    Full Name: <input name='full_name' required><br><br>
    Phone: <input name='phone' required><br><br>
    Status: <input name='status' value='Active'><br><br>
    <button type='submit'>Save</button>
    </form><a href='/admin-dashboard/'>Back</a>
    """)

def edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        member.member_no = request.POST.get('member_no')
        member.full_name = request.POST.get('full_name')
        member.phone = request.POST.get('phone')
        member.status = request.POST.get('status')
        member.save()
        return redirect('/admin-dashboard/')
    return HttpResponse(f"""
    <h2>Edit Member</h2>
    <form method='post'>
    Member No: <input name='member_no' value='{member.member_no}' required><br><br>
    Full Name: <input name='full_name' value='{member.full_name}' required><br><br>
    Phone: <input name='phone' value='{member.phone}' required><br><br>
    Status: <input name='status' value='{member.status}'><br><br>
    <button type='submit'>Update</button>
    </form><a href='/admin-dashboard/'>Back</a>
    """)

def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.delete()
    return redirect('/admin-dashboard/')
