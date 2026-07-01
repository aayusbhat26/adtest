from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging

from .repository import TodoRepository, TodoStore

logger = logging.getLogger(__name__)


class TodoListView(APIView):
    repository_factory = TodoRepository

    def get_repository(self) -> TodoStore:
        if not hasattr(self, "_repository"):
            self._repository = self.repository_factory()
        return self._repository

    def get(self, request):
        try:
            todos = self.get_repository().get_all()
            return Response(todos, status=status.HTTP_200_OK)
        except Exception:
            logger.exception("Error in GET /todos")
            return Response(
                {"error": "Failed to fetch todos"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            title = request.data.get("title", "").strip()
            if not title:
                return Response(
                    {"error": "Title is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            created_todo = self.get_repository().create(title)

            return Response(created_todo, status=status.HTTP_201_CREATED)
        except Exception:
            logger.exception("Error in POST /todos")
            return Response(
                {"error": "Failed to create todo"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )