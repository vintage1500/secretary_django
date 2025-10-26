from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Question

from django.db import models  # for F expressions
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.decorators import action

from .models import User, QuestionCategory, QuestionSubcategory, StaticQuestion, DynamicQuestion
from .serializers import (
    UserSerializer,
    QuestionCategorySerializer,
    QuestionSubcategorySerializer,
    StaticQuestionSerializer,
    DynamicQuestionSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "chat_id"  # let the bot address by chat_id

    @action(detail=False, methods=["get"], url_path=r"exists/(?P<chat_id>\d+)")
    def exists(self, request, chat_id=None):
        return Response({"exists": User.objects.filter(chat_id=chat_id).exists()})

    @action(detail=False, methods=["get"], url_path=r"is-admin/(?P<chat_id>\d+)")
    def is_admin(self, request, chat_id=None):
        val = User.objects.filter(chat_id=chat_id).values_list("administrator", flat=True).first()
        return Response({"administrator": bool(val)})

    @action(detail=False, methods=["get"], url_path=r"info/(?P<chat_id>\d+)")
    def info(self, request, chat_id=None):
        user = get_object_or_404(User, chat_id=chat_id)
        return Response({
            "last_name": user.last_name,
            "first_name": user.first_name,
            "patronymic": user.patronymic,
            "us_group": user.us_group,
            "administrator": user.administrator,
        })

    @action(detail=False, methods=["get"], url_path=r"first-name/(?P<chat_id>\d+)")
    def first_name(self, request, chat_id=None):
        user = get_object_or_404(User, chat_id=chat_id)
        return Response({"first_name": user.first_name})

    @action(detail=False, methods=["get"], url_path=r"user-id/(?P<chat_id>\d+)")
    def user_id(self, request, chat_id=None):
        uid = User.objects.filter(chat_id=chat_id).values_list("user_id", flat=True).first()
        return Response({"user_id": uid})


class QuestionCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = QuestionCategory.objects.all().order_by("category_id")
    serializer_class = QuestionCategorySerializer
    lookup_field = "category_id"

    @action(detail=False, methods=["get"], url_path=r"by-name/(?P<name>.+)")
    def by_name(self, request, name=None):
        category = get_object_or_404(QuestionCategory, name=name)
        return Response({"category_id": category.category_id, "name": category.name})


class QuestionSubcategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = QuestionSubcategory.objects.select_related("category").all()
    serializer_class = QuestionSubcategorySerializer
    lookup_field = "subcategory_id"

    @action(detail=False, methods=["get"], url_path=r"by-category/(?P<category_id>\d+)")
    def by_category(self, request, category_id=None):
        data = QuestionSubcategory.objects.filter(category_id=category_id).values("subcategory_id", "name")
        return Response(list(data))

    @action(detail=True, methods=["get"], url_path="description")
    def description(self, request, pk=None):
        sub = self.get_object()
        return Response({"name": sub.name, "description": sub.description})


class StaticQuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StaticQuestion.objects.select_related("category").all()
    serializer_class = StaticQuestionSerializer
    lookup_field = "static_question_id"

    @action(detail=False, methods=["get"], url_path=r"by-category-name/(?P<name>.+)")
    def by_category_name(self, request, name=None):
        category = get_object_or_404(QuestionCategory, name=name)
        qs = StaticQuestion.objects.filter(category=category)
        return Response(StaticQuestionSerializer(qs, many=True).data)


class DynamicQuestionViewSet(mixins.CreateModelMixin,
                             mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             viewsets.GenericViewSet):
    queryset = DynamicQuestion.objects.select_related("user", "category").all()
    serializer_class = DynamicQuestionSerializer
    lookup_field = "dynamic_question_id"

    @action(detail=False, methods=["get"], url_path=r"by-category-unanswered/(?P<name>.+)")
    def by_category_unanswered(self, request, name=None):
        qs = (DynamicQuestion.objects
              .filter(category__name=name, answer=False)
              .select_related("user", "category"))
        data = qs.values(
            last_name=models.F("user__last_name"),
            first_name=models.F("user__first_name"),
            patronymic=models.F("user__patronymic"),
            us_group=models.F("user__us_group"),
            username=models.F("user__username"),
            category=models.F("category__name"),
            description=models.F("description"),
        )
        return Response(list(data))


@api_view(['POST'])
def create_question(request):
    try:
        data = request.data
        Question.objects.create(
            user_type=data.get('user_type'),
            username=data.get('username'),
            question_text=data.get('question')
        )
        return Response({"status": "ok"}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
