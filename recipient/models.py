from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Recipient(models.Model):
    """
    Модель для тех, кому рассылаем
    """
    email = models.EmailField(verbose_name='Почта', unique=True)
    name = models.CharField(max_length=100, verbose_name='Имя')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name='Владелец'
    )

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'
        permissions = [
            ("can_view_client", "Can view recipient"),
            ("can_delete_client", "Can delete recipient"),
            ("can_edit_client", "Can edit recipient"),
        ]

    def __str__(self):
        return self.email
