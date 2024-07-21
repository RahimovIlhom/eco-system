from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import EcoBranchEmployee, RegisteredQRCode
from .serializers import (EmployeesListSerializer, RegisteredQRCodesListSerializer, WinnersListSerializer,
                          WinnerDetailSerializer)
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
        return RegisteredQRCode.objects.filter(qrcode__game__id=game_id, winner=False)

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        game_id = self.request.query_params.get('game_id')
        return RegisteredQRCode.objects.filter(qrcode__game__id=game_id, winner=True)

    @swagger_auto_schema(
        operation_description="Get list of winners",
        responses={
            200: WinnersListSerializer(many=True),
            400: openapi.Response(description="Game ID kiritilmadi!"),
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


class CreateWinnerAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WinnerDetailSerializer

    @swagger_auto_schema(
        operation_description="Create winner",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'registered_qrcode_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the registered QR code"),
            },
            required=['registered_qrcode_id'],
        ),
        responses={
            200: WinnerDetailSerializer,
            400: openapi.Response(
                description="Invalid input",
                examples={
                    "application/json": {
                        "detail": "Ro'yxatdan o'tkazilgan QR kod kiritilmadi!"
                    }
                }
            ),
            404: openapi.Response(
                description="Winner not found",
                examples={
                    "application/json": {
                        "detail": "Bunday ID da ro'yxatdan o'tkazilgan QR kod topilmadi!"
                    }
                }
            )
        },
    )
    def post(self, request, *args, **kwargs):
        registered_qrcode_id = request.data.get('registered_qrcode_id')
        if not registered_qrcode_id:
            return Response({"detail": "Ro'yxatdan o'tkazilgan QR kod kiritilmadi!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            registered_qrcode = RegisteredQRCode.objects.get(id=registered_qrcode_id)
        except RegisteredQRCode.DoesNotExist:
            return Response({"detail": "Bunday ID da ro'yxatdan o'tkazilgan QR kod topilmadi!"}, status=status.HTTP_404_NOT_FOUND)

        print(registered_qrcode)
        if registered_qrcode.winner:
            return Response({"detail": "Bunday ID da ro'yxatdan o'tkazilgan QR kod allaqchon yutuq egasi!"}, status=status.HTTP_400_BAD_REQUEST)

        registered_qrcode.winner = True
        registered_qrcode.save()
        serializer = self.serializer_class(instance=registered_qrcode)
        return Response(serializer.data)
