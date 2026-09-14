from django.contrib import admin

from .models import BankAccount


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):

    list_display = [
        "account_number",
        "owner",
        "account_type",
        "currency",
        "balance",
        "status",
        "created_at",
    ]

    list_filter = [
        "account_type",
        "currency",
        "status",
    ]

    search_fields = [
        "account_number",
        "owner__email",
        "owner__first_name",
        "owner__last_name",
    ]

    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    ordering = [
        "-created_at"
    ]