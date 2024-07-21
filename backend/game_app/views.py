from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Game
from .serializers import GamesListSerializer


class GameListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Game.objects.all()
    serializer_class = GamesListSerializer
