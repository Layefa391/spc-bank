from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):

    list_display = [
        "reference",
        "account",
        "transaction_type",
        "amount",
        "status",
        "created_by",
        "created_at",
    ]

    list_filter = [
        "transaction_type",
        "status",
        "created_at",
    ]

    search_fields = [
        "reference",
        "account__account_number",
        "account__owner__email",
    ]

    readonly_fields = [
        "reference",
    ]

    ordering = [
        "-created_at"
    ]