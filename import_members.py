import os
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from members.models import Member

print("Loading members from full_backup.json...")

try:
    with open('full_backup.json', 'r') as f:
        data = json.load(f)
    
    count = 0
    for m in data:
        Member.objects.update_or_create(
            member_number=m['member_number'],
            defaults={
                'name': m['name'],
                'phone_number': m['phone_number'],
                'status': m.get('status', 'ACTIVE')
            }
        )
        count += 1
    
    print(f"✅ SUCCESSFULLY IMPORTED {count} MEMBERS - PERMANENT!")
    
except FileNotFoundError:
    print("full_backup.json not found, skipping import")
except Exception as e:
    print(f"Error: {e}")
