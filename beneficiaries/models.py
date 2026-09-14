from django.conf import settings
from django.db import models

from banking.models import BankAccount


class Beneficiary(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="beneficiaries",
    )

    account = models.ForeignKey(
        BankAccount,
        on_delete=models.PROTECT,
        related_name="beneficiaries",
    )

    nickname = models.CharField(
        max_length=100,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "account"],
                name="unique_beneficiary_per_owner",
            )
        ]

    def __str__(self):
        if self.nickname:
            return f"{self.nickname} - {self.account.account_number}"

        return f"{self.account.owner.get_full_name()} - {self.account.account_number}"