from django.core.management.base import BaseCommand
from users.models import User
from django_seed import Seed


class Command(BaseCommand):

    help = "It seeds the DB with tons of stuff"

    def handle(self, *args, **options):

        user_seed = Seed.seeder()
        user_seed.add_entity(
            User,
            30,
            {
                "is_staff": False,
                "is_superuser": False,
                "social_platform": None,
                "social_login_id": None,
            },
        )
        user_seed.execute()
        self.stdout.write(self.style.SUCCESS("Users seeded"))
