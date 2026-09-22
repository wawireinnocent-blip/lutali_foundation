from .models import Member
from django.contrib.auth.models import User

MEMBERS_32 = [
    ('LUT-001','ISAAC FRED','0768760386','active',False),
    ('LUT-002','Esther Luchivia','0792967633','active',False),
    ('LUT-003','Ajella Mulari','0759531836','active',False),
    ('LUT-004','INNOCENT WAWIRE','0703416356','active',True), # ADMIN
    ('LUT-005','Laban Fula','0111410769','active',False),
    ('LUT-006','KenPeter Muchika','0768075466','active',False),
    ('LUT-007','Melvin Barasa','0797969333','active',False),
    ('LUT-008','Mildred Lumbasi','0707397500','active',False),
    ('LUT-009','Leah Juma','0701434949','active',False),
    ('LUT-010','Yvonne Kharinda','0759221476','active',False),
    ('LUT-011','Christine Zipporah','0742023615','active',False),
    ('LUT-012','Alex Koikoi','0706313051','active',False),
    ('LUT-013','Joshua Sindani','0791279560','active',False),
    ('LUT-014','Emmanuel Sunguti','0727994764','active',False),
    ('LUT-015','Cedrick Chivuyi','0705890849','active',False),
    ('LUT-016','Mildred Nekesa','0713364628','active',False),
    ('LUT-017','Burntone Kulova','0700602172','active',False),
    ('LUT-018','Isaiah Wete','0758795051','active',False),
    ('LUT-019','Austin Mando','0715244622','active',False),
    ('LUT-020','Ali Kibaya','0798911493','active',False),
    ('LUT-021','Philemon Tom','0748343436','active',False),
    ('LUT-022','Nicole Nakhumicha','0796610007','inactive',False), # INACTIVE
    ('LUT-023','Mercyline Mutenyo','0707828521','active',False),
    ('LUT-024','Salome Salim','0795983430','active',False),
    ('LUT-025','Leah Salim','0729010826','active',False),
    ('LUT-026','John Museve','0798709891','active',False),
    ('LUT-027','Esther Kharinda','0707277721','active',False),
    ('LUT-028','Gloria Imbiakha','0743166089','inactive',False), # INACTIVE
    ('LUT-029','Daniel Solomon','0758570045','active',False),
    ('LUT-030','Elizabeth Muhonja','0795313500','active',False),
    ('LUT-031','Gelda Weyala','0712694179','active',False),
    ('LUT-032','Yvonne Mwenesi','0787849794','inactive',False), # INACTIVE
]

def seed_32():
    if Member.objects.count() >= 32:
        return
    Member.objects.all().delete()
    User.objects.filter(username__startswith='07').delete()
    User.objects.filter(username__startswith='01').delete()
    for no,name,phone,status,is_admin in MEMBERS_32:
        user,_ = User.objects.get_or_create(username=phone)
        user.set_password(no) # LUT-XXX as password
        user.save()
        m = Member.objects.create(member_no=no, full_name=name, phone=phone, status=status, is_admin=is_admin, user=user)
        # Registration 100 for ALL 32
        from .models import Bill
        Bill.objects.create(member=m, bill_type='Registration', amount=100, description='Registration Day 1')
    # Backup admin login LUT-004 + kuks17231#
    admin_user,_ = User.objects.get_or_create(username='LUT-004')
    admin_user.set_password('kuks17231#')
    admin_user.save()
