from django.core.management.base import BaseCommand
from ...models import User


class Command(BaseCommand):
    help = 'Create a superuser with specified credentials'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            help='Email address of the superuser'
        )
        parser.add_argument(
            '--password',
            type=str,
            help='Password for the superuser'
        )

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']

        if not email or not password:
            self.stdout.write(self.style.ERROR(
                    'Error: Email and password are required'
                ))
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(
                f'Error: User with email "{email}" already exists'
            ))
            return

        user = User.objects.create(email=email, password=password)
        user.is_superuser = True
        user.save()
        self.stdout.write(
            self.style.SUCCESS(f'Superuser "{email}" created successfully')
        )
