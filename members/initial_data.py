from django.contrib.auth.models import User
from members.models import Member
INITIAL_MEMBERS=[
{"full_name":"ISAAC FRED","member_no":"LUT-001","phone":"0768760386","status":"active","is_admin":False},
{"full_name":"Esther Luchivia","member_no":"LUT-002","phone":"0792967633","status":"active","is_admin":False},
{"full_name":"Ajella Mulari","member_no":"LUT-003","phone":"0759531836","status":"active","is_admin":False},
{"full_name":"INNOCENT WAWIRE","member_no":"LUT-004","phone":"0703416356","status":"active","is_admin":True},
{"full_name":"Laban Fula","member_no":"LUT-005","phone":"0111410769","status":"active","is_admin":False},
{"full_name":"KenPeter Muchika","member_no":"LUT-006","phone":"0768075466","status":"active","is_admin":False},
{"full_name":"Melvin Barasa","member_no":"LUT-007","phone":"0797969333","status":"active","is_admin":False},
{"full_name":"Mildred Lumbasi","member_no":"LUT-008","phone":"0707397500","status":"active","is_admin":False},
{"full_name":"Leah Juma","member_no":"LUT-009","phone":"0701434949","status":"active","is_admin":False},
{"full_name":"Yvonne Kharinda","member_no":"LUT-010","phone":"0759221476","status":"active","is_admin":False},
{"full_name":"Christine Zipporah","member_no":"LUT-011","phone":"0742023615","status":"active","is_admin":False},
{"full_name":"Alex Koikoi","member_no":"LUT-012","phone":"0706313051","status":"active","is_admin":False},
{"full_name":"Joshua Sindani","member_no":"LUT-013","phone":"0791279560","status":"active","is_admin":False},
{"full_name":"Emmanuel Sunguti","member_no":"LUT-014","phone":"0727994764","status":"active","is_admin":False},
{"full_name":"Cedrick Chivuyi","member_no":"LUT-015","phone":"0705890849","status":"active","is_admin":False},
{"full_name":"Mildred Nekesa","member_no":"LUT-016","phone":"0713364628","status":"active","is_admin":False},
{"full_name":"Burntone Kulova","member_no":"LUT-017","phone":"0700602172","status":"active","is_admin":False},
{"full_name":"Isaiah Wete","member_no":"LUT-018","phone":"0758795051","status":"active","is_admin":False},
{"full_name":"Austin Mando","member_no":"LUT-019","phone":"0715244622","status":"active","is_admin":False},
{"full_name":"Ali Kibaya","member_no":"LUT-020","phone":"0798911493","status":"active","is_admin":False},
{"full_name":"Philemon Tom","member_no":"LUT-021","phone":"0748343436","status":"active","is_admin":False},
{"full_name":"Nicole Nakhumicha","member_no":"LUT-022","phone":"0796610007","status":"inactive","is_admin":False},
{"full_name":"Mercyline Mutenyo","member_no":"LUT-023","phone":"0707828521","status":"active","is_admin":False},
{"full_name":"Salome Salim","member_no":"LUT-024","phone":"0795983430","status":"active","is_admin":False},
{"full_name":"Leah Salim","member_no":"LUT-025","phone":"0729010826","status":"active","is_admin":False},
{"full_name":"John Museve","member_no":"LUT-026","phone":"0798709891","status":"active","is_admin":False},
{"full_name":"Esther Kharinda","member_no":"LUT-027","phone":"0707277721","status":"active","is_admin":False},
{"full_name":"Gloria Imbiakha","member_no":"LUT-028","phone":"0743166089","status":"inactive","is_admin":False},
{"full_name":"Daniel Solomon","member_no":"LUT-029","phone":"0758570045","status":"active","is_admin":False},
{"full_name":"Elizabeth Muhonja","member_no":"LUT-030","phone":"0795313500","status":"active","is_admin":False},
{"full_name":"Gelda Weyala","member_no":"LUT-031","phone":"0712694179","status":"active","is_admin":False},
{"full_name":"Yvonne Mwenesi","member_no":"LUT-032","phone":"0787849794","status":"inactive","is_admin":False},
]
def seed_members():
    from finance.models import Billing
    for d in INITIAL_MEMBERS:
        m,created=Member.objects.get_or_create(member_no=d['member_no'],defaults={'full_name':d['full_name'],'phone':d['phone'],'status':d['status'],'is_admin':d['is_admin']})
        if not User.objects.filter(username=d['phone']).exists():
            u=User.objects.create_user(username=d['phone'],password=d['member_no']); m.user=u; m.save()
        if d['member_no']=='LUT-004' and not User.objects.filter(username='LUT-004').exists():
            User.objects.create_user(username='LUT-004',password='kuks17231#')
        if created:
            Billing.objects.get_or_create(member=m,billing_type='registration',defaults={'amount':100,'description':'Registration 100'})