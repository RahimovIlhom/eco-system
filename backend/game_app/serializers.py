from rest_framework import serializers
from .models import Game, QRCode
from users.models import RegisteredQRCode


class GamesListSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField('get_count')

    class Meta:
        model = Game
        fields = ['id', 'name_uz', 'name_ru', 'description_uz', 'description_ru', 'start_date', 'end_date', 'status', 'count']

    def get_count(self, obj):
        return RegisteredQRCode.objects.filter(qrcode__game__id=obj.id).count()


class QRCodeSerializer(serializers.ModelSerializer):
    eco_branch_name_uz = serializers.SerializerMethodField('get_eco_branch_uz')
    eco_branch_name_ru = serializers.SerializerMethodField('get_eco_branch_ru')

    class Meta:
        model = QRCode
        fields = ['id', 'code', 'eco_branch_name_uz', 'eco_branch_name_ru']

    def get_eco_branch_uz(self, obj):
        return obj.eco_branch.name_uz

    def get_eco_branch_ru(self, obj):
        return obj.eco_branch.name_ru
