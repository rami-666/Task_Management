from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import Signal, post_save
from django.dispatch import receiver
from django.db.models import signals
from task_manager.tasks import send_task_assignment_email

task_assigned = Signal()


# Create your models here.
class Priority(models.Model):
    priority = models.CharField(max_length=20)

    def __str__(self):
        return self.priority


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True)
    priority = models.ForeignKey(Priority, on_delete=models.DO_NOTHING, null=True)
    due_date = models.DateField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.title


@receiver(task_assigned)
def handle_task_assignment(sender, task, **kwargs):
    assigned_user = task.user
    print(f"TASK ASSIGNED TO: {assigned_user.email}")
    send_task_assignment_email.delay(assigned_user.email, task.title, task.priority.priority, task.due_date)


@receiver(post_save, sender=Task)
def task_assignment_signal_handler(sender, instance, created, **kwargs):
    if created:
        task_assigned.send(sender=Task, task=instance)
