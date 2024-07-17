from django.contrib import admin

from .models import EcoBranchEmployee, Participant, RegisteredQRCode, Winner


@admin.register(EcoBranchEmployee)
class EcoBranchEmployeeAdmin(admin.ModelAdmin):
    list_display = ['tg_id', 'employee', 'eco_branch', 'fullname', 'phone', 'inn', ]
    list_filter = ['employee', 'eco_branch']


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['tg_id', 'fullname', 'phone', 'address', 'location', ]


@admin.register(RegisteredQRCode)
class RegisteredQRCodeAdmin(admin.ModelAdmin):
    list_display = ['participant', 'qrcode', 'location', 'created_at']


@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ['registered_qrcode', 'created_at']
