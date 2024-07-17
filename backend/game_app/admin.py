from django.contrib import admin

from .models import Game, QRCode


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'start_date', 'end_date', 'status', 'employee')


@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'game', 'eco_branch', 'is_active', 'activity_time')
