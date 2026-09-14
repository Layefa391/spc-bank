from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BeneficiaryForm
from .models import Beneficiary


@login_required
def beneficiaries_view(request):
    beneficiaries = (
        Beneficiary.objects
        .filter(owner=request.user)
        .select_related("account", "account__owner")
    )

    if request.method == "POST":
        form = BeneficiaryForm(
            request.POST,
            owner=request.user,
        )

        if form.is_valid():
            Beneficiary.objects.create(
                owner=request.user,
                account=form.cleaned_account,
                nickname=form.cleaned_data["nickname"].strip(),
            )

            return redirect("beneficiaries")
    else:
        form = BeneficiaryForm(
            owner=request.user,
        )

    return render(
        request,
        "beneficiaries/list.html",
        {
            "beneficiaries": beneficiaries,
            "form": form,
        },
    )


@login_required
def delete_beneficiary(request, beneficiary_id):
    beneficiary = get_object_or_404(
        Beneficiary,
        id=beneficiary_id,
        owner=request.user,
    )

    if request.method == "POST":
        beneficiary.delete()

    return redirect("beneficiaries")