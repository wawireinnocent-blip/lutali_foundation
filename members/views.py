from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Member

@login_required
def admin_dashboard(request):
    members = Member.objects.all().order_by('member_number')
    active_count = members.filter(status='ACTIVE').count()
    inactive_count = members.filter(status='INACTIVE').count()
    total_count = members.count()
    
    context = {
        'members': members,
        'active_count': active_count,
        'inactive_count': inactive_count,
        'total_count': total_count,
    }
    return render(request, 'admin_dashboard.html', context)

@login_required
def add_member(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        member_number = request.POST.get('member_number')
        phone_number = request.POST.get('phone_number')
        status = request.POST.get('status', 'ACTIVE')
        
        Member.objects.create(
            name=name,
            member_number=member_number,
            phone_number=phone_number,
            status=status
        )
        messages.success(request, f'{name} ameongezwa!')
        return redirect('admin_dashboard')
    return redirect('admin_dashboard')

@login_required
def edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        member.name = request.POST.get('name')
        member.member_number = request.POST.get('member_number')
        member.phone_number = request.POST.get('phone_number')
        member.status = request.POST.get('status')
        member.save()
        messages.success(request, 'Member updated!')
        return redirect('admin_dashboard')
    return redirect('admin_dashboard')

@login_required
def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.delete()
    messages.success(request, 'Member deleted!')
    return redirect('admin_dashboard')

def home(request):
    members = Member.objects.filter(status='ACTIVE')
    return render(request, 'home.html', {'members': members})
