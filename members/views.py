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
        rows = "<tr><td colspan='5' style='text-align:center;padding:20px;color:red'><b>DATABASE IS EMPTY!<br>Go to Render > Shell and run: python import_members.py</b></td></tr>"

    html = f"""
    <html><head><title>Lutali Admin</title>
    <style>body{{font-family:Arial;padding:20px}}table{{width:100%;border-collapse:collapse}}th,td{{border:1px solid #ccc;padding:10px}}th{{background:#333;color:#fff}}a{{text-decoration:none}}</style>
    </head><body>
    <h1>Lutali Foundation - Members ({count})</h1>
    <a href='/add-member/' style='background:green;color:white;padding:10px 15px;border-radius:5px'>+ ADD MEMBER</a>
    <br><br>
    <table><tr><th>Member No</th><th>Full Name</th><th>Phone</th><th>Status</th><th>Action</th></tr>
    {rows}
    </table>
    <br><br><p>Live URL: https://lutali-foundation-4x36.onrender.com/admin-dashboard/</p>
    </body></html>
    """
    return HttpResponse(html)

@csrf_exempt
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
    <form method='POST'>
    Member No: <input name='member_no' required><br><br>
    Full Name: <input name='full_name' required><br><br>
    Phone: <input name='phone' required><br><br>
    Status: <input name='status' value='Active'><br><br>
    <button type='submit'>SAVE</button>
    </form><br><a href='/admin-dashboard/'>Back to Dashboard</a>
    """)

@csrf_exempt
def edit_member(request, member_id):
    m = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        m.member_no = request.POST.get('member_no')
        m.full_name = request.POST.get('full_name')
        m.phone = request.POST.get('phone')
        m.status = request.POST.get('status')
        m.save()
        return redirect('/admin-dashboard/')
    return HttpResponse(f"""
    <h2>Edit {m.full_name}</h2>
    <form method='POST'>
    Member No: <input name='member_no' value='{m.member_no}' required><br><br>
    Full Name: <input name='full_name' value='{m.full_name}' required><br><br>
    Phone: <input name='phone' value='{m.phone}' required><br><br>
    Status: <input name='status' value='{m.status}'><br><br>
    <button type='submit'>UPDATE</button>
    </form><br><a href='/admin-dashboard/'>Back</a>
    """)

def delete_member(request, member_id):
    m = get_object_or_404(Member, id=member_id)
    m.delete()
    return redirect('/admin-dashboard/')
