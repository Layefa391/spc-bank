from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = "Reset the SPC Bank admin password."

    def handle(self, *args, **options):
        email = "layefamulade@gmail.com"
        new_password = "Spctest@2026"

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"No user found with email: {email}")
            )
            return

        user.set_password(new_password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(
            update_fields=[
                "password",
                "is_staff",
                "is_superuser",
                "is_active",
            ]
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"Admin password reset successfully for {email}"
            )
        )