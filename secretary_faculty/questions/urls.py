from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    QuestionCategoryViewSet,
    QuestionSubcategoryViewSet,
    StaticQuestionViewSet,
    DynamicQuestionViewSet,
)

router = DefaultRouter()
router.register(r"api/users", UserViewSet, basename="users")
router.register(r"api/categories", QuestionCategoryViewSet, basename="categories")
router.register(r"api/subcategories", QuestionSubcategoryViewSet, basename="subcategories")
router.register(r"api/static-questions", StaticQuestionViewSet, basename="static-questions")
router.register(r"api/dynamic-questions", DynamicQuestionViewSet, basename="dynamic-questions")

urlpatterns = [
    path('api/questions/create/', views.create_question),
    path("", include(router.urls))
]