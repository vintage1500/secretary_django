from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Question

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
