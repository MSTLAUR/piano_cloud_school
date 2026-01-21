from django.db import models
import requests


def get_client_ip(request):
    """Get the client's IP address from the request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_location_from_ip(ip):
    """Get location data from IP address using ipapi.co."""
    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/')
        data = response.json()
        return {
            'country': data.get('country_name'),
            'city': data.get('city'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude')
        }
    except:
        return None


class EmailLead(models.Model):
    
    FEATURE_CHOICES = [
        ('scheduling', '📅 Better Scheduling'),
        ('payments', '💰 Flexible Payments'),
        ('messaging', '💬 In-App Messaging'),
        ('digital', '📦 Digital Products'),
        ('reports', '📊 Financial Reports'),
        ('mobile', '📱 Mobile App')
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    feature = models.CharField(max_length=20, choices=FEATURE_CHOICES, blank=True, null=True)
    comment = models.TextField(blank=True)
    
    # Geolocation fields
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    def __str__(self):
        return self.email



    
    
    
    