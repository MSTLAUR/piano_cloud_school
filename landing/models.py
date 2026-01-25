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
    if not ip or ip == '127.0.0.1':
        return None
    
    try:
        response = requests.get(
            f'https://ipapi.co/{ip}/json/',
            timeout=3  # 3 second timeout to prevent hanging
        )
        
        # Check if request was successful
        if response.status_code != 200:
            return None
            
        data = response.json()
        
        # Check if API returned an error
        if 'error' in data:
            return None
        
        return {
            'country': data.get('country_name'),
            'city': data.get('city'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude')
        }
    except (requests.RequestException, ValueError, KeyError) as e:
        # Log error in production for debugging
        print(f"IP geolocation error for {ip}: {str(e)}")
        return None
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Unexpected error in get_location_from_ip: {str(e)}")
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



    
    
    
    