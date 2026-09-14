from decimal import Decimal
import uuid

from django.db import transaction as db_transaction

from banking.models import BankAccount
from transactions.models import Transaction


def generate_reference():
    return f"SPC-{uuid.uuid4().hex[:12].upper()}"


@db_transaction.atomic
def deposit(account, amount, user, description="Cash deposit"):
    amount = Decimal(str(amount))

    if amount <= 0:
        raise ValueError("Deposit amount must be greater than zero.")

    account = BankAccount.objects.select_for_update().get(
        pk=account.pk
    )

    account.balance += amount
    account.save(update_fields=["balance", "updated_at"])

    return Transaction.objects.create(
        reference=generate_reference(),
        account=account,
        transaction_type=Transaction.TransactionType.DEPOSIT,
        direction=Transaction.TransactionDirection.CREDIT,
        amount=amount,
        description=description,
        status=Transaction.TransactionStatus.COMPLETED,
        created_by=user,
    )


@db_transaction.atomic
def withdraw(account, amount, user, description="Cash withdrawal"):
    amount = Decimal(str(amount))

    if amount <= 0:
        raise ValueError("Withdrawal amount must be greater than zero.")

    account = BankAccount.objects.select_for_update().get(
        pk=account.pk
    )

    if amount > account.balance:
        raise ValueError("Insufficient funds.")

    account.balance -= amount
    account.save(update_fields=["balance", "updated_at"])

    return Transaction.objects.create(
        reference=generate_reference(),
        account=account,
        transaction_type=Transaction.TransactionType.WITHDRAWAL,
        direction=Transaction.TransactionDirection.DEBIT,
        amount=amount,
        description=description,
        status=Transaction.TransactionStatus.COMPLETED,
        created_by=user,
    )
def transfer(sender_account, recipient_account, amount, user, description="Bank transfer"):
    amount = Decimal(str(amount))

    if amount <= 0:
        raise ValueError("Transfer amount must be greater than zero.")

    if sender_account.pk == recipient_account.pk:
        raise ValueError("You cannot transfer money to your own account.")

    if sender_account.status != BankAccount.AccountStatus.ACTIVE:
        raise ValueError("Your account is not active.")

    if recipient_account.status != BankAccount.AccountStatus.ACTIVE:
        raise ValueError("Recipient account is not active.")

    if sender_account.currency != recipient_account.currency:
        raise ValueError("Currency mismatch between accounts.")

    if sender_account.balance < amount:
        raise ValueError("Insufficient funds.")

    with db_transaction.atomic():

        # Lock accounts in a consistent order to reduce deadlock risk.
        account_ids = sorted([sender_account.pk, recipient_account.pk])

        locked_accounts = (
            BankAccount.objects
            .select_for_update()
            .filter(pk__in=account_ids)
            .order_by("pk")
        )

        accounts = {account.pk: account for account in locked_accounts}

        sender = accounts[sender_account.pk]
        recipient = accounts[recipient_account.pk]

        # Re-check the balance after acquiring the database lock.
        if sender.balance < amount:
            raise ValueError("Insufficient funds.")

        sender.balance -= amount
        recipient.balance += amount

        sender.save(update_fields=["balance", "updated_at"])
        recipient.save(update_fields=["balance", "updated_at"])

        transfer_reference = generate_reference()

        sender_transaction = Transaction.objects.create(
            reference=transfer_reference + "-D",
            account=sender,
            transaction_type=Transaction.TransactionType.TRANSFER,
            direction=Transaction.TransactionDirection.DEBIT,
            amount=amount,
            description=description or f"Transfer to {recipient.account_number}",
            status=Transaction.TransactionStatus.COMPLETED,
            created_by=user,
        )

        Transaction.objects.create(
            reference=transfer_reference + "-C",
            account=recipient,
            transaction_type=Transaction.TransactionType.TRANSFER,
            direction=Transaction.TransactionDirection.CREDIT,
            amount=amount,
            description=description or f"Transfer from {sender.account_number}",
            status=Transaction.TransactionStatus.COMPLETED,
            created_by=user,
        )

        return sender_transaction