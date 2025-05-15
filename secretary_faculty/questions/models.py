from django.db import models

class Question(models.Model):
    USER_TYPE_CHOICES = [
        ('applicant', 'Абитуриент'),
        ('student', 'Студент'),
    ]
    
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        verbose_name='Тип пользователя'
    )
    question_text = models.TextField(verbose_name='Текст вопроса')
    username = models.CharField(
        max_length=100,
        verbose_name='Telegram username',
        blank=True,
        null=True
    )
    is_processed = models.BooleanField(
        default=False,
        verbose_name='Обработан ли вопрос'
    )
    admin_comment = models.TextField(
        verbose_name='Комментарий администратора',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_user_type_display()}: {self.question_text[:50]}..."