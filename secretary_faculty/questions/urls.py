from django.urls import path
from . import views

urlpatterns = [
    path('api/questions/create/', views.create_question),
]