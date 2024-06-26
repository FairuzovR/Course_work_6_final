from ...models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Создание суперпользователя
    """
    def handle(self, *args, **options):
        user = User.objects.create()
        user.username = 'SU_CMD_2'
        user.email = 'superuser@su.su'
        user.set_password('12345')
        user.is_superuser = True
        user.is_staff = True
