from django import forms

from banking.models import BankAccount
from .models import Beneficiary


class BeneficiaryForm(forms.Form):
    account_number = forms.CharField(
        max_length=10,
        min_length=10,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter 10-digit SPC Bank account number",
                "inputmode": "numeric",
            }
        ),
    )

    nickname = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "e.g. David, Mom, John",
            }
        ),
    )

    def __init__(self, *args, owner=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.owner = owner

    def clean_account_number(self):
        account_number = self.cleaned_data["account_number"].strip()

        try:
            account = BankAccount.objects.select_related("owner").get(
                account_number=account_number
            )
        except BankAccount.DoesNotExist:
            raise forms.ValidationError(
                "No SPC Bank account was found with this account number."
            )

        if self.owner and account.owner_id == self.owner.id:
            raise forms.ValidationError(
                "You cannot add your own account as a beneficiary."
            )

        if self.owner and Beneficiary.objects.filter(
            owner=self.owner,
            account=account,
        ).exists():
            raise forms.ValidationError(
                "This account is already in your beneficiaries."
            )

        if account.status != BankAccount.AccountStatus.ACTIVE:
            raise forms.ValidationError(
                "This account is not currently active."
            )

        self.cleaned_account = account

        return account_number