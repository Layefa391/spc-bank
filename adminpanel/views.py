from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

from accounts.models import User
from banking.models import BankAccount
from transactions.models import Transaction


def admin_check(user):
    return user.is_authenticated and (
        user.is_staff or user.is_superuser
    )


@user_passes_test(admin_check)
def admin_dashboard(request):
    customers = User.objects.filter(role=User.Role.CUSTOMER)

    context = {
        "total_customers": customers.count(),
        "total_accounts": BankAccount.objects.count(),
        "total_transactions": Transaction.objects.count(),
        "total_balance": sum(
            account.balance
            for account in BankAccount.objects.all()
        ),
        "recent_transactions": Transaction.objects.select_related(
            "account",
            "account__owner"
        )[:10],
        "recent_customers": customers.order_by("-date_joined")[:8],
    }

    return render(
        request,
        "adminpanel/dashboard.html",
        context,
    )