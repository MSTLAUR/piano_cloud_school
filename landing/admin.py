from django.contrib import admin
from .models import EmailLead


@admin.register(EmailLead)
class EmailLeadAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'feature', 'comment', 'created_at']
    search_fields = ['email', 'first_name', 'feature', 'comment']
    list_filter = ['created_at']
    readonly_fields = ['created_at']