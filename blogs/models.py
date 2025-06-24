from django.db import models


class Post(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Заголовок",
        help_text="Введите заголовок",
    )

    content = models.TextField(
        verbose_name="Содержание",
        help_text="Введите содержание",
    )

    preview = models.ImageField(
        upload_to="post/preview",
        blank=True,
        null=True,
        verbose_name="Превью(изображение)",
        help_text="Загрузите фото(изображение)",
    )

    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )

    publication_sign = models.BooleanField(
        default=False,
        verbose_name="Признак публикации",
    )

    views_count = models.PositiveIntegerField(
        verbose_name="Счетчик просмотров",
        help_text="Укажите количество просмотров",
        default=0,
    )

    class Meta:
        verbose_name = "запись"
        verbose_name_plural = "записи"

    def __str__(self):
        return self.title
