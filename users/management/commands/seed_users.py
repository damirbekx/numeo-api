from django.core.management.base import BaseCommand
from users.models import User
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Seeds the database with fake users'

    def add_arguments(self, parser):
        parser.add_argument('num_users', type=int, help='The number of fake users to create.')
        parser.add_argument('--batch-size', type=int, default=10000, help='Batch size for bulk create.')

    def handle(self, *args, **options):
        target_total = options['num_users']
        batch_size = options['batch_size']

        current_count = User.objects.count()
        if current_count >= target_total:
            self.stdout.write(self.style.SUCCESS(f'Database already has {current_count} users. Skipping seeding.'))
            return

        users_needed = target_total - current_count
        fake = Faker()

        self.stdout.write(self.style.SUCCESS(f'Current count: {current_count}. Seeding {users_needed} more users in batches of {batch_size}...'))

        total_created = 0
        while total_created < users_needed:
            current_batch_count = min(batch_size, users_needed - total_created)
            users_to_create = []

            for _ in range(current_batch_count):
                first_name = fake.first_name()
                last_name = fake.last_name()
                email = f"{first_name.lower()}.{last_name.lower()}.{random.randint(1, 1000000)}@{fake.free_email_domain()}"

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

            User.objects.bulk_create(users_to_create, ignore_conflicts=True)
            total_created += current_batch_count
            self.stdout.write(f'Created {total_created}/{users_needed} users (Total: {current_count + total_created})...')

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded. Final count: {User.objects.count()}'))
