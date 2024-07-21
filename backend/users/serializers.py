from rest_framework import serializers

from .models import EcoBranchEmployee, Participant, RegisteredQRCode
from eco_app.serializers import EcoBranchSerializer
from game_app.serializers import QRCodeSerializer


class EmployeesListSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField('get_id')
    eco_branch = EcoBranchSerializer(read_only=True)

    class Meta:
        model = EcoBranchEmployee
        fields = ['id', 'language', 'eco_branch', 'fullname', 'phone', 'inn', 'created_at', 'updated_at']
        ref_name = 'UsersEmployeesListSerializer'

    def get_id(self, obj):
        return obj.tg_id


class ParticipantSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField('get_id')

    class Meta:
        model = Participant
        fields = ['id', 'language', 'fullname', 'phone']
        ref_name = 'UsersParticipantSerializer'

    def get_id(self, obj):
        return obj.tg_id


class RegisteredQRCodesListSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer(read_only=True)
    qrcode = QRCodeSerializer(read_only=True)

    class Meta:
        model = RegisteredQRCode
        fields = ['id', 'participant', 'qrcode', 'created_at', 'updated_at']
        ref_name = 'UsersRegisteredQRCodesListSerializer'


class WinnersListSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer(read_only=True)
    qrcode = QRCodeSerializer(read_only=True)

    class Meta:
        model = RegisteredQRCode
        fields = ['id', 'participant', 'qrcode', 'created_at', 'updated_at']
        ref_name = 'UsersWinnersListSerializer'


class WinnerDetailSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer(read_only=True)
    qrcode = QRCodeSerializer(read_only=True)

    class Meta:
        model = RegisteredQRCode
        fields = ['id', 'participant', 'qrcode', 'winner', 'created_at', 'updated_at']
        ref_name = 'UsersWinnerDetailsSerializer'
