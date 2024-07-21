from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import EcoBranchEmployee, RegisteredQRCode, Winner
from .serializers import EmployeesListSerializer, RegisteredQRCodesListSerializer, WinnersListSerializer
from game_app.models import Game, QRCode


class EmployeesListAPIView(generics.ListAPIView):
    serializer_class = EmployeesListSerializer
    queryset = EcoBranchEmployee.objects.all()
    permission_classes = [IsAuthenticated]


class RegisteredQRCodesListAPIView(generics.ListAPIView):
    serializer_class = RegisteredQRCodesListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        game_id = self.request.query_params.get('game_id')
        return RegisteredQRCode.objects.filter(qrcode__game__id=game_id)

    @swagger_auto_schema(
        operation_description="Get list of registered QR codes",
        responses={
            200: RegisteredQRCodesListSerializer(many=True),
            404: openapi.Response(description="Game not found",
                                  examples={"application/json": {"detail": "Bunday ID da konkurs topilmadi!"}})
        },
        manual_parameters=[
            openapi.Parameter('game_id', openapi.IN_QUERY, description="ID of the game", type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self, request, *args, **kwargs):
        game_id = self.request.query_params.get('game_id')
        if not game_id:
            return Response({"detail": "Game ID kiritilmadi!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response({"detail": "Bunday ID da konkurs topilmadi!"}, status=status.HTTP_404_NOT_FOUND)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class WinnersListAPIView(generics.ListAPIView):
    serializer_class = WinnersListSerializer
    queryset = Winner.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        game_id = self.request.query_params.get('game_id')
        return Winner.objects.filter(registered_qrcode__qrcode__game__id=game_id)

    @swagger_auto_schema(
        operation_description="Get list of winners",
        responses={
            200: WinnersListSerializer(many=True),
            404: openapi.Response(description="Game not found",
                                  examples={"application/json": {"detail": "Bunday ID da konkurs topilmadi!"}})
        },
        manual_parameters=[
            openapi.Parameter('game_id', openapi.IN_QUERY, description="ID of the game", type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self, request, *args, **kwargs):
        game_id = self.request.query_params.get('game_id')
        if not game_id:
            return Response({"detail": "Game ID kiritilmadi!"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            Game.objects.get(id=game_id)
        except Game.DoesNotExist:
            return Response({"detail": "Bunday ID da konkurs topilmadi!"}, status=status.HTTP_404_NOT_FOUND)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
