from django.contrib import admin

from .models import EcoBranchEmployee, Participant, RegisteredQRCode, PlasticCard


@admin.register(EcoBranchEmployee)
class EcoBranchEmployeeAdmin(admin.ModelAdmin):
    list_display = ['tg_id', 'eco_branch', 'fullname', 'phone', 'inn', ]
    list_filter = ['eco_branch']


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['tg_id', 'fullname', 'phone', 'created_at', 'updated_at']


@admin.register(RegisteredQRCode)
class RegisteredQRCodeAdmin(admin.ModelAdmin):
    list_display = ['participant', 'qrcode', 'location', 'created_at']


@admin.register(PlasticCard)
class PlasticCardAdmin(admin.ModelAdmin):
    list_display = ['participant', 'card_type']
