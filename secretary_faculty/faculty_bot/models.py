from django.db import models
from .managers.obj_manager import UserManager, StaticQuestionManager, DynamicQuestionManager, QuestionCategoryManager, QuestionSubcategoryManager

class QuestionCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    objects = QuestionCategoryManager()
    
    def __str__(self):
        return self.name

class QuestionSubcategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(
        QuestionCategory, 
        on_delete=models.CASCADE,
        related_name='subcategories'
    )
    
    objects = QuestionSubcategoryManager()
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"

class User(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    us_group = models.CharField(max_length=50)
    username = models.CharField(max_length=100)
    administrator = models.BooleanField(default=False)
    chat_id = models.BigIntegerField(unique=True)
    
    objects = UserManager()
    
    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.us_group})"

class StaticQuestion(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        QuestionCategory,
        on_delete=models.CASCADE,
        related_name='static_questions'
    )
    answer = models.TextField()
    
    objects = StaticQuestionManager()
    
    def __str__(self):
        return self.name

class DynamicQuestion(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='dynamic_questions'
    )
    description = models.TextField()
    category = models.ForeignKey(
        QuestionCategory,
        on_delete=models.CASCADE,
        related_name='dynamic_questions'
    )
    answer = models.BooleanField(default=False)
    
    objects = DynamicQuestionManager()
    
    def __str__(self):
        return f"Вопрос от {self.user} ({self.category.name})"