from django.contrib import admin
from .models import Question

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('user_type', 'question_text', 'created_at')
    list_filter = ('user_type', 'created_at')
    search_fields = ('question_text',)
    date_hierarchy = 'created_at'