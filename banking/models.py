import random
from decimal import Decimal

from django.conf import settings
from django.db import models


def generate_account_number():
    while True:
        number = str(random.randint(1000000000, 9999999999))

        if not BankAccount.objects.filter(account_number=number).exists():
            return number


class BankAccount(models.Model):

    class AccountType(models.TextChoices):
        SAVINGS = "SAVINGS", "Savings Account"
        CURRENT = "CURRENT", "Current Account"

    class AccountStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        SUSPENDED = "SUSPENDED", "Suspended"
        CLOSED = "CLOSED", "Closed"

    account_number = models.CharField(
        max_length=10,
        unique=True,
        db_index=True,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="bank_accounts",
    )

    account_type = models.CharField(
        max_length=20,
        choices=AccountType.choices,
        default=AccountType.SAVINGS,
    )

    currency = models.CharField(
        max_length=3,
        default="USD",
    )

    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    status = models.CharField(
        max_length=20,
        choices=AccountStatus.choices,
        default=AccountStatus.ACTIVE,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = generate_account_number()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.account_number} - {self.owner.email}"

    class Meta:
        ordering = ["-created_at"]