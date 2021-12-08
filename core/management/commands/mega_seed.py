import random
from django.core.management.base import BaseCommand
from users.models import User
from mypage.models import Profile
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

        profiles = Profile.objects.all()

        for profile in profiles[50:]:
            profile.image = f"media/default/{random.randint(1,7)}.png"
            profile.save()
        self.stdout.write(self.style.SUCCESS("Profile seeded"))
