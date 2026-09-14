import uuid
from decimal import Decimal

from django.db import transaction as db_transaction

from banking.models import BankAccount
from transactions.models import Transaction


def generate_transfer_reference():
    return f"SPC-TRF-{uuid.uuid4().hex[:10].upper()}"


@db_transaction.atomic
def transfer_money(sender_account, recipient_account, amount, user, description=""):
    amount = Decimal(str(amount))

    if amount <= 0:
        raise ValueError("Transfer amount must be greater than zero.")

    if sender_account.pk == recipient_account.pk:
        raise ValueError("You cannot transfer money to your own account.")

    # Lock accounts in a consistent order.
    account_ids = sorted([sender_account.pk, recipient_account.pk])

    locked_accounts = {
        account.pk: account
        for account in BankAccount.objects.select_for_update().filter(
            pk__in=account_ids
        )
    }

    sender = locked_accounts[sender_account.pk]
    recipient = locked_accounts[recipient_account.pk]

    if sender.status != BankAccount.AccountStatus.ACTIVE:
        raise ValueError("Your account is not active.")

    if recipient.status != BankAccount.AccountStatus.ACTIVE:
        raise ValueError("The recipient's account is not active.")

    if sender.currency != recipient.currency:
        raise ValueError("Currency mismatch between accounts.")

    if amount > sender.balance:
        raise ValueError("Insufficient funds.")

    sender.balance -= amount
    recipient.balance += amount

    sender.save(update_fields=["balance", "updated_at"])
    recipient.save(update_fields=["balance", "updated_at"])

    reference = generate_transfer_reference()

    Transaction.objects.create(
        reference=reference,
        account=sender,
        transaction_type=Transaction.TransactionType.TRANSFER,
        amount=amount,
        description=description or f"Transfer to {recipient.account_number}",
        status=Transaction.TransactionStatus.COMPLETED,
        created_by=user,
    )

    Transaction.objects.create(
        reference=f"{reference}-CR",
        account=recipient,
        transaction_type=Transaction.TransactionType.TRANSFER,
        amount=amount,
        description=description or f"Transfer from {sender.account_number}",
        status=Transaction.TransactionStatus.COMPLETED,
        created_by=user,
    )

    return reference