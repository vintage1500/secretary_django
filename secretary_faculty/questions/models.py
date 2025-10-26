from django.db import models

class User(models.Model):
    class Meta:
        db_table = "users"
        constraints = [
            models.UniqueConstraint(fields=["chat_id"], name="users_chat_id_key"),
        ]
        indexes = [
            models.Index(fields=["chat_id"], name="users_chat_id_idx"),
            models.Index(fields=["username"], name="users_username_idx"),
        ]

    user_id = models.BigAutoField(primary_key=True)  # GENERATED ALWAYS AS IDENTITY
    last_name = models.TextField()
    first_name = models.TextField()
    patronymic = models.TextField()
    us_group = models.TextField()
    username = models.TextField()
    administrator = models.BooleanField(default=False)
    chat_id = models.BigIntegerField(unique=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} (@{self.username})"


class QuestionCategory(models.Model):
    class Meta:
        db_table = "question_categories"
        indexes = [
            models.Index(fields=["name"], name="qcat_name_idx"),
        ]

    category_id = models.BigAutoField(primary_key=True)
    name = models.TextField(unique=True)

    def __str__(self):
        return self.name


class QuestionSubcategory(models.Model):
    class Meta:
        db_table = "question_subcategories"
        indexes = [
            models.Index(fields=["category"], name="qsubcat_category_idx"),
        ]

    subcategory_id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField()
    category = models.ForeignKey(
        QuestionCategory,
        on_delete=models.CASCADE,
        db_column="category_id",
        related_name="subcategories",
        null=True,
    )

    def __str__(self):
        return f"{self.name} ({self.category_id})"


class StaticQuestion(models.Model):
    class Meta:
        db_table = "static_questions"
        indexes = [
            models.Index(fields=["category"], name="squest_category_idx"),
            models.Index(fields=["name"], name="squest_name_idx"),
        ]

    static_question_id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    category = models.ForeignKey(
        QuestionCategory,
        on_delete=models.CASCADE,
        db_column="category_id",
        related_name="static_questions",
    )
    answer = models.TextField()

    def __str__(self):
        return f"{self.name}"


class DynamicQuestion(models.Model):
    class Meta:
        db_table = "dynamic_questions"
        indexes = [
            models.Index(fields=["category"], name="dquest_category_idx"),
            models.Index(fields=["user"], name="dquest_user_idx"),
            models.Index(fields=["answer"], name="dquest_answer_idx"),
        ]

    dynamic_question_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="dynamic_questions",
    )
    description = models.TextField()
    category = models.ForeignKey(
        QuestionCategory,
        on_delete=models.CASCADE,
        db_column="category_id",
        related_name="dynamic_questions",
    )
    answer = models.BooleanField(default=False)

    def __str__(self):
        return f"Question by {self.user_id} in {self.category_id}"


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