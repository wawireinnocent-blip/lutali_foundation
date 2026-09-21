import os, django, json, re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lutali.settings')
django.setup()
from members.models import Member

with open('members32.json') as f:
    members=json.load(f)

c=0
for row in members:
    if Member.objects.filter(member_number=row['member_number']).exists():
        continue
    Member.objects.create(
        name=row['name'],
        member_number=row['member_number'],
        phone_number=re.sub(r'[^0-9]','',row['phone']),
        is_active=row['status']=='ACTIVE'
    )
    c+=1
print(f"Imported {c}, Total {Member.objects.count()}")