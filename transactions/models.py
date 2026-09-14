import uuid

from django.conf import settings
from django.db import models


def generate_transaction_reference():
    return uuid.uuid4().hex[:32]


class Transaction(models.Model):

    class TransactionType(models.TextChoices):
        DEPOSIT = "DEPOSIT", "Deposit"
        WITHDRAWAL = "WITHDRAWAL", "Withdrawal"
        TRANSFER = "TRANSFER", "Transfer"

    class TransactionStatus(models.TextChoices):
        COMPLETED = "COMPLETED", "Completed"
        PENDING = "PENDING", "Pending"
        FAILED = "FAILED", "Failed"

    reference = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        default=generate_transaction_reference,
    )

    account = models.ForeignKey(
        "banking.BankAccount",
        on_delete=models.PROTECT,
        related_name="transactions",
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TransactionType.choices,
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
    )

    description = models.CharField(
        max_length=255,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=TransactionStatus.choices,
        default=TransactionStatus.COMPLETED,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="created_transactions",
    )

    created_at = models.DateTimeField()
    def __str__(self):
        return f"{self.reference} - {self.amount}"

    class Meta:
        ordering = ["-created_at"]