from django.db.models.signals import Signal
from django.dispatch import receiver
from django.db.models import signals

task_assigned = Signal()