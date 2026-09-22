import os
import sys
import json

# Hakikisha Django inapata settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'lutali'))
sys.path.append(os.path.join(BASE_DIR, 'lutali_foundation'))

# Jaribu settings zote
for mod in ['settings', 'lutali.settings', 'lutali_foundation.settings']:
    try:
        os.environ['DJANGO_SETTINGS_MODULE'] = mod
        import django
        django.setup()
        print(f"Using settings: {mod}")
        break
    except:
        continue

from members.models import Member

print("Loading from full_backup.json...")
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
    
    print(f"✅ IMPORTED {count} MEMBERS - HAWATAPOTEA TENA!")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
