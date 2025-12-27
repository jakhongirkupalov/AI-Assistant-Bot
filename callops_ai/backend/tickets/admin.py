from django.contrib import admin
from .models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("user_id", "message")

    fields = (
        "user_id",
        "message",
        "answer",
        "status",
    )

    readonly_fields = ("user_id", "message")
