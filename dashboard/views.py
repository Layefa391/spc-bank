from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    account = request.user.bank_accounts.first()

    return render(
        request,
        "dashboard/dashboard.html",
        {
            "account": account,
        },
    )