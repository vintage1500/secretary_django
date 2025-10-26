from rest_framework import serializers
from .models import User, QuestionCategory, QuestionSubcategory, StaticQuestion, DynamicQuestion

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "user_id",
            "last_name",
            "first_name",
            "patronymic",
            "us_group",
            "username",
            "administrator",
            "chat_id",
        )
        read_only_fields = ("user_id",)


class QuestionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionCategory
        fields = ("category_id", "name")
        read_only_fields = ("category_id",)


class QuestionSubcategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = QuestionSubcategory
        fields = ("subcategory_id", "name", "description", "category", "category_name")
        read_only_fields = ("subcategory_id",)


class StaticQuestionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = StaticQuestion
        fields = ("static_question_id", "name", "category", "category_name", "answer")
        read_only_fields = ("static_question_id",)


class DynamicQuestionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    user_chat_id = serializers.IntegerField(source="user.chat_id", read_only=True)

    class Meta:
        model = DynamicQuestion
        fields = (
            "dynamic_question_id",
            "user",
            "user_chat_id",
            "description",
            "category",
            "category_name",
            "answer",
        )
        read_only_fields = ("dynamic_question_id",)
