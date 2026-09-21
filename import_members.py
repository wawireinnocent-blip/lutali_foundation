import os, django, json, re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lutali_foundation.settings')
django.setup()
from members.models import Member

try:
    with open('members32.json') as f:
        members = json.load(f)
    count=0
    for row in members:
        m_no = row['member_number'].strip()
        if Member.objects.filter(member_number=m_no).exists():
            continue
        Member.objects.create(
            name=row['name'].strip(),
            member_number=m_no,
            phone_number=re.sub(r'[^0-9]','',row['phone']),
            is_active=(row['status']=='ACTIVE')
        )
        count+=1
    print(f"Imported {count} members. Total {Member.objects.count()}")
except Exception as e:
    print(f"Import skipped: {e}")