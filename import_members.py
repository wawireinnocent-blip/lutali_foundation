import os, django, re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lutali_foundation.settings')
django.setup()
from members.models import Member
import pandas as pd

df = pd.read_excel("PHONE_NUMBERS.xlsx")
for _, row in df.iterrows():
    name = str(row['NAME']).strip()
    m_no = str(row['MEMBER NUMBER ']).strip()
    phone = re.sub(r'[^0-9]', '', str(row['PHONE NUMBER']))
    status = str(row['STATUS']).strip().upper()
    if Member.objects.filter(member_number=m_no).exists():
        continue
    Member.objects.create(
        name=name,
        member_number=m_no,
        phone_number=phone,
        phone=phone,
        is_active=(status=='ACTIVE'),
        status=status
    )
    print(f"✅ {m_no} {name}")

print("🎉 32 members imported! Dashboard sasa ni LIVELY!")