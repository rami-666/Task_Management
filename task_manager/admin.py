from django.contrib import admin
from .models import (
    Task,
    Priority,
)

# Register your models here.

admin.site.register(Priority)


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "priority")
    list_filter = ("user",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)
        return qs


admin.site.register(Task, TaskAdmin)
