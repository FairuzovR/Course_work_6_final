from django.db import models

from users.models import User

NULLABLE = {"null": True, "blank": True}


class Blog(models.Model):
    """
    Модель для блога
    """
    title = models.CharField(max_length=250, verbose_name="Заголовок")
    body = models.TextField(verbose_name="Содержимое")
    image = models.ImageField(
        upload_to="blog/",
        verbose_name="Изображение",
        **NULLABLE
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Признак публикации"
    )
    view_count = models.IntegerField(
        default=0,
        verbose_name="Количество просмотров"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        **NULLABLE,
        verbose_name="Владелец"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "блог"
        verbose_name_plural = "блоги"
        permissions = [
            ("can_edit_blog", "Права на изменение блога"),
            ("can_delete_blog", "Права на удаление блога"),
            ("can_add_blog", "Права на добавление блога"),
        ]
