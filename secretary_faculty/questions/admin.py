from django.contrib import admin
from .models import Question

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('user_type', 'question_text', 'username', 'is_processed', 'created_at')
    list_filter = ('user_type', 'created_at', 'is_processed')
    search_fields = ('question_text', 'username')
    date_hierarchy = 'created_at'
    list_editable = ('is_processed',)
    fieldsets = (
        (None, {
            'fields': ('user_type', 'username', 'question_text', 'is_processed', 'admin_comment')
        }),
    )