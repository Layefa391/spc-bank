from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from banking.models import BankAccount
from .forms import CustomerRegistrationForm


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            BankAccount.objects.create(
                owner=user,
                account_type=BankAccount.AccountType.SAVINGS,
                currency="USD",
                balance=0,
            )

            login(request, user)
            return redirect("dashboard")
    else:
        form = CustomerRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            email=email,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(
            request,
            "accounts/login.html",
            {"error": "Invalid email or password."},
        )

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")