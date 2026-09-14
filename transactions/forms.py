from django import forms

from banking.models import BankAccount


class AmountForm(forms.Form):
    amount = forms.DecimalField(
        min_value=0.01,
        max_digits=15,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                "placeholder": "0.00",
                "step": "0.01",
                "min": "0.01",
            }
        ),
    )

    description = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Optional description"
            }
        ),
    )


class TransferForm(forms.Form):
    recipient_account = forms.CharField(
        max_length=10,
        min_length=10,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter 10-digit account number",
                "inputmode": "numeric",
            }
        ),
    )

    amount = forms.DecimalField(
        min_value=0.01,
        max_digits=15,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                "placeholder": "0.00",
                "step": "0.01",
                "min": "0.01",
            }
        ),
    )

    description = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "placeholder": "What is this transfer for?"
            }
        ),
    )

    def clean_recipient_account(self):
        account_number = self.cleaned_data["recipient_account"].strip()

        try:
            account = BankAccount.objects.get(
                account_number=account_number
            )
        except BankAccount.DoesNotExist:
            raise forms.ValidationError(
                "No SPC Bank account was found with this account number."
            )

        return account