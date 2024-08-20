from celery import shared_task
from .models import EcoBranch
from django.utils import timezone


@shared_task
def update_is_active():
    now = timezone.now()
    branches = EcoBranch.objects.filter(is_active=True, activity_time__lte=now)
    branches.update(is_active=False)
