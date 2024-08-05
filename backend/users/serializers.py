from rest_framework import serializers

from .models import EcoBranchEmployee, Participant, RegisteredQRCode, PlasticCard
from eco_app.serializers import EcoBranchSerializer
from game_app.serializers import QRCodeSerializer
from utils import decrypt_data


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


class CardSerializer(serializers.ModelSerializer):
    card_number = serializers.SerializerMethodField('get_card_number')

    class Meta:
        model = PlasticCard
        fields = ['id', 'participant', 'card_type', 'card_number', 'card_date', 'card_cvv', 'bank_name', 'card_image', 'created_at', 'updated_at']

    def get_card_number(self, obj):
        return decrypt_data(obj.card_number)


class WinnersListSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer(read_only=True)
    qrcode = QRCodeSerializer(read_only=True)
    card = serializers.SerializerMethodField('get_card')

    class Meta:
        model = RegisteredQRCode
        fields = ['id', 'participant', 'qrcode', 'card', 'created_at', 'updated_at']
        ref_name = 'UsersWinnersListSerializer'

    def get_card(self, obj):
        participant = obj.participant
        card = PlasticCard.objects.filter(participant=participant).first()
        return CardSerializer(instance=card).data


class WinnerDetailSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer(read_only=True)
    qrcode = QRCodeSerializer(read_only=True)

    class Meta:
        model = RegisteredQRCode
        fields = ['id', 'participant', 'qrcode', 'winner', 'created_at', 'updated_at']
        ref_name = 'UsersWinnerDetailsSerializer'
