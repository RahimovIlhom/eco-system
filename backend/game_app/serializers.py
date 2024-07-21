from rest_framework import serializers
from .models import Game, QRCode


class GamesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'


class QRCodeSerializer(serializers.ModelSerializer):
    eco_branch_name = serializers.SerializerMethodField('get_eco_branch')

    class Meta:
        model = QRCode
        fields = ['id', 'code', 'eco_branch_name']

    def get_eco_branch(self, obj):
        return obj.eco_branch.name
