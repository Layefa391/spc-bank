from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from banking.models import BankAccount
from banking.services.transfer_service import transfer_money

from .forms import AmountForm, TransferForm
from .models import Transaction
from .services import deposit, withdraw


@login_required
def deposit_view(request):
    account = request.user.bank_accounts.first()

    if account is None:
        return render(
            request,
            "transactions/deposit.html",
            {
                "account": None,
                "error": "No bank account is associated with this user.",
            },
        )

    if request.method == "POST":
        form = AmountForm(request.POST)

        if form.is_valid():
            try:
                deposit(
                    account=account,
                    amount=form.cleaned_data["amount"],
                    user=request.user,
                    description=form.cleaned_data["description"]
                    or "Cash deposit",
                )

                return redirect("dashboard")

            except ValueError as error:
                form.add_error("amount", str(error))

    else:
        form = AmountForm()

    return render(
        request,
        "transactions/deposit.html",
        {
            "account": account,
            "form": form,
        },
    )


@login_required
def withdraw_view(request):
    account = request.user.bank_accounts.first()

    if account is None:
        return render(
            request,
            "transactions/withdraw.html",
            {
                "account": None,
                "error": "No bank account is associated with this user.",
            },
        )

    if request.method == "POST":
        form = AmountForm(request.POST)

        if form.is_valid():
            try:
                withdraw(
                    account=account,
                    amount=form.cleaned_data["amount"],
                    user=request.user,
                    description=form.cleaned_data["description"]
                    or "Cash withdrawal",
                )

                return redirect("dashboard")

            except ValueError as error:
                form.add_error("amount", str(error))

    else:
        form = AmountForm()

    return render(
        request,
        "transactions/withdraw.html",
        {
            "account": account,
            "form": form,
        },
    )


@login_required
def transfer_view(request):
    account = request.user.bank_accounts.first()

    if account is None:
        return redirect("dashboard")

    # Get beneficiary account from the URL when coming
    # from the Beneficiaries page.
    recipient_account = request.GET.get("recipient", "").strip()

    if request.method == "POST":
        form = TransferForm(request.POST)

        if form.is_valid():
            recipient = form.cleaned_data["recipient_account"]

            try:
                transfer_money(
                    sender_account=account,
                    recipient_account=recipient,
                    amount=form.cleaned_data["amount"],
                    user=request.user,
                    description=form.cleaned_data["description"],
                )

                return redirect("transactions")

            except ValueError as error:
                form.add_error("amount", str(error))

    else:
        form = TransferForm(
            initial={
                "recipient_account": recipient_account,
            }
        )

    return render(
        request,
        "transactions/transfer.html",
        {
            "account": account,
            "form": form,
        },
    )


@login_required
def transactions_view(request):
    account = request.user.bank_accounts.first()

    transactions = (
        Transaction.objects
        .filter(account=account)
        .select_related("account")
    )

    return render(
        request,
        "transactions/history.html",
        {
            "account": account,
            "transactions": transactions,
        },
    )
@login_required
def transaction_detail_view(request, reference):
    account = request.user.bank_accounts.first()

    transaction = (
        Transaction.objects
        .filter(
            account=account,
            reference=reference,
        )
        .select_related("account")
        .first()
    )

    if transaction is None:
        return redirect("transactions")

    return render(
        request,
        "transactions/detail.html",
        {
            "account": account,
            "transaction": transaction,
        },
    )