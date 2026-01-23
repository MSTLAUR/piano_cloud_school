from django.contrib import admin
from .models import EmailLeadJournalist


@admin.register(EmailLeadJournalist)
class EmailLeadJournalistAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'feature', 'comment', 'created_at', 'country', 'city']
    search_fields = ['email', 'first_name', 'feature', 'comment', 'country', 'city']
    list_filter = ['created_at', 'feature', 'country']
    readonly_fields = ['created_at', 'ip_address', 'country', 'city', 'latitude', 'longitude']

    fieldsets = (
        ('Contact Information', {
            'fields': ('email', 'first_name')
        }),
        ('Feedback', {
            'fields': ('feature', 'comment')
        }),
        ('Geolocation Data', {
            'fields': ('ip_address', 'country', 'city', 'latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',)
        }),
    )
