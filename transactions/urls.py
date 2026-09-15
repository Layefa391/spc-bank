from django.urls import path

from .views import (
    deposit_view,
    transaction_detail_view,
    transactions_view,
    transfer_view,
    withdraw_view,
)

urlpatterns = [
    path("deposit/", deposit_view, name="deposit"),
    path("withdraw/", withdraw_view, name="withdraw"),
    path("transfer/", transfer_view, name="transfer"),
    path(
        "<str:reference>/",
        transaction_detail_view,
        name="transaction_detail",
    ),
    path("", transactions_view, name="transactions"),
]