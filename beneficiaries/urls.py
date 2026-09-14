from django.urls import path

from .views import beneficiaries_view, delete_beneficiary


urlpatterns = [
    path("", beneficiaries_view, name="beneficiaries"),
    path(
        "delete/<int:beneficiary_id>/",
        delete_beneficiary,
        name="delete_beneficiary",
    ),
]