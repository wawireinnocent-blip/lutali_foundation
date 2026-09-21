import os, django, re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lutali.settings')
django.setup()
from members.models import Member
import openpyxl

try:
    wb = openpyxl.load_workbook("PHONE_NUMBERS.xlsx")
    ws = wb.active
    count=0
    # Skip header row
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row[0]:
            continue
        name = str(row[0]).strip()
        m_no = str(row[1]).strip()
        phone_raw = str(row[2])
        status = str(row[3]).strip().upper() if row[3] else "ACTIVE"
        phone = re.sub(r'[^0-9]', '', phone_raw)

        if Member.objects.filter(member_number=m_no).exists():
            continue

        Member.objects.create(
            name=name,
            member_number=m_no,
            phone_number=phone,
            is_active=(status=="ACTIVE")
        )
        count+=1
        print(f"✅ {m_no} {name}")
    print(f"🎉 Imported {count} | Total {Member.objects.count()}")
except Exception as e:
    print(f"Import error but build continues: {e}")