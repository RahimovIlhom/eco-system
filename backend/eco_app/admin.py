from django.contrib import admin

from .models import EcoBranch

from .translation import EcoBranchTranslationOptions


@admin.register(EcoBranch)
class EcoBranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'working_days')
    list_filter = ('working_days', )
    search_fields = ('name', 'working_days')
