from django.core.management.base import BaseCommand
from users.models import User
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Seeds the database with fake users'

    def add_arguments(self, parser):
        parser.add_argument('num_users', type=int, help='The number of fake users to create.')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding users...'))
        fake = Faker()
        num_users = options['num_users']

        users_to_create = []
        for _ in range(num_users):
            first_name = fake.first_name()
            last_name = fake.last_name()

            # Ensure unique emails
            email = f"{first_name.lower()}.{last_name.lower()}.{random.randint(1, 10000)}@{fake.free_email_domain()}"

            users_to_create.append(
                User(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    age=random.randint(18, 99),
                    country=fake.country(),
                    city=fake.city(),
                    occupation=fake.job(),
                    phone_number=fake.phone_number(),
                    birth_date=fake.date_of_birth(minimum_age=18, maximum_age=90),
                    address=fake.address(),
                    bio=fake.text(max_nb_chars=200),
                    is_active=fake.boolean(chance_of_getting_true=90),
                )
            )

        # Bulk create users for efficiency
        User.objects.bulk_create(users_to_create, ignore_conflicts=True)
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {len(users_to_create)} users.'))
