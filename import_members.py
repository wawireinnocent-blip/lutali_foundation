import os, django, re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lutali.settings')
django.setup()
from members.models import Member
import openpyxl

wb = openpyxl.load_workbook("PHONE_NUMBERS.xlsx")
ws = wb.active

added = 0
for row in ws.iter_rows(min_row=2, values_only=True):
    if not row or not row[0]:
        continue
    name = str(row[0]).strip()
    m_no = str(row[1]).strip()
    phone = re.sub(r'[^0-9]','', str(row[2] or ''))
    status = str(row[3] or 'ACTIVE').upper()

    obj, created = Member.objects.get_or_create(
        member_number=m_no,
        defaults={
            'name': name,
            'phone_number': phone,
            'is_active': status == 'ACTIVE'
        }
    )
    if created:
        added += 1
        print(f"✅ {m_no} {name}")

print(f"🎉 Added {added} new | Total in cloud: {Member.objects.count()}")