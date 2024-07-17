from django.contrib import admin

from .models import EcoBranch


@admin.register(EcoBranch)
class EcoBranchAdmin(admin.ModelAdmin):
    list_display = ('address', 'working_days')
    list_filter = ('address', 'working_days')
    search_fields = ('address', 'working_days')
