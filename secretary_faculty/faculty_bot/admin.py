from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'us_group', 'administrator')
    search_fields = ('last_name', 'first_name', 'us_group', 'chat_id')
    list_filter = ('administrator', 'us_group')

@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(QuestionSubcategory)
class QuestionSubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'description')
    list_filter = ('category',)

@admin.register(StaticQuestion)
class StaticQuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'answer')
    list_filter = ('category',)

@admin.register(DynamicQuestion)
class DynamicQuestionAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'answer')
    search_fields = ('description',)
    list_filter = ('category', 'answer')
    raw_id_fields = ('user',)