import os
import django
import json

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'termproject.settings')  # Replace 'projectname' with your project folder name

# Initialize Django
django.setup()

from django.core.serializers import serialize
from charactercreator.models import BackgroundBond, HangUp, Perk

# Serialize the data
data = {
    'BackgroundBond': json.loads(serialize('json', BackgroundBond.objects.all())),
    'HangUp': json.loads(serialize('json', HangUp.objects.all())),
    'Influence': json.loads(serialize('json', BackgroundBond.objects.all())),
    'Perk': json.loads(serialize('json', Perk.objects.all())),
}

# Write data to a JSON file
with open('core_rulebook.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=2, ensure_ascii=False)  # Use ensure_ascii=False to handle special characters
