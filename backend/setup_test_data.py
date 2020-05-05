import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "interview_code_test.settings")

import django
django.setup()

from tasks.models import Task


Task.objects.create(
    category=Task.Category.moving.key,
    name='test',
    description='test desc',
)
