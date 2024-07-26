from django.contrib import admin

from .models import Game, QRCode, GameInfo

from .translation import GameTranslationOptions


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'start_date', 'end_date', 'status')


@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'game', 'eco_branch', 'is_active', 'activity_time')


@admin.register(GameInfo)
class GameInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'image_url')
    list_filter = ('title', 'description')
