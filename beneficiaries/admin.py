from django.contrib import admin

from .models import Beneficiary


@admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = [
        "nickname",
        "owner",
        "account",
        "created_at",
    ]

    search_fields = [
        "nickname",
        "owner__email",
        "owner__first_name",
        "owner__last_name",
        "account__account_number",
    ]

    list_filter = [
        "created_at",
    ]

    readonly_fields = [
        "created_at",
    ]

    ordering = [
        "-created_at",
    ]