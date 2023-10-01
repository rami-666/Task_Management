import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from task_manager.models import Task, Priority


def create_regular_users_group():
    # Get the content type of the Task model
    content_type = ContentType.objects.get_for_model(Task)

    # Create the Regular Users group
    regular_users_group, created = Group.objects.get_or_create(name="Regular Users")

    # Get the permissions for the Task model
    permissions = Permission.objects.filter(content_type=content_type)

    updated_permissions = [x for x in permissions[1:]]

    print(f"Permissions: {updated_permissions}")

    # Add the permissions to the Regular Users group
    regular_users_group.permissions.set(updated_permissions)

    print("Regular Users group created successfully!")


def create_priorities():
    priorities = ["low", "medium", "high"]

    for priority in priorities:
        Priority.objects.get_or_create(priority=priority)

    print("Priorities created successfully!")


if __name__ == "__main__":
    create_regular_users_group()
    create_priorities()
