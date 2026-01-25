from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .forms import WaitlistForm, FeedbackForm
from .models import get_client_ip, get_location_from_ip


def home_view(request):
    waitlist_form = WaitlistForm()
    feedback_form = FeedbackForm()

    context = {
        'waitlist_form': waitlist_form,
        'feedback_form': feedback_form,
    }

    return render(request, 'landing/home.html', context)


def waitlist_submit(request):
    if request.method == 'POST':
        form = WaitlistForm(request.POST)
        if form.is_valid():
            try:
                # Get IP address and location data
                lead = form.save(commit=False)
                lead.ip_address = get_client_ip(request)
                
                # Try to get location, but don't fail if it doesn't work
                try:
                    location_data = get_location_from_ip(lead.ip_address)
                    if location_data:
                        lead.country = location_data.get('country')
                        lead.city = location_data.get('city')
                        lead.latitude = location_data.get('latitude')
                        lead.longitude = location_data.get('longitude')
                except Exception as e:
                    # Log but don't fail - geolocation is optional
                    print(f"Geolocation failed: {str(e)}")
                
                lead.save()
            except Exception as e:
                # Log the actual error for debugging
                print(f"Error saving waitlist lead: {str(e)}")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'errors': {'error': ['An error occurred. Please try again.']}
                    }, status=500)
                else:
                    messages.error(request, 'An error occurred. Please try again.')
                    return redirect('landing:home')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Thanks for joining! We\'ll be in touch soon.',
                    'redirect_url': '/thanks/'
                })
            else:
                messages.success(request, 'Thanks for joining! We\'ll be in touch soon.')
                return redirect('landing:thanks')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
            else:
                messages.error(request, 'Please check your email and try again.')
                return redirect('landing:home')
    return redirect('landing:home')


def feedback_submit(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            try:
                # Get IP address and location data
                lead = form.save(commit=False)
                lead.ip_address = get_client_ip(request)
                
                # Try to get location, but don't fail if it doesn't work
                try:
                    location_data = get_location_from_ip(lead.ip_address)
                    if location_data:
                        lead.country = location_data.get('country')
                        lead.city = location_data.get('city')
                        lead.latitude = location_data.get('latitude')
                        lead.longitude = location_data.get('longitude')
                except Exception as e:
                    # Log but don't fail - geolocation is optional
                    print(f"Geolocation failed: {str(e)}")
                
                lead.save()
            except Exception as e:
                # Log the actual error for debugging
                print(f"Error saving feedback: {str(e)}")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'errors': {'error': ['An error occurred. Please try again.']}
                    }, status=500)
                else:
                    messages.error(request, 'An error occurred. Please try again.')
                    return redirect('landing:home')
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you for your feedback!',
                    'redirect_url': '/thanks/'
                })
            else:
                messages.success(request, 'Thank you for your feedback!')
                return redirect('landing:thanks')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
            else:
                messages.error(request, 'Please complete the form and try again.')
                return redirect('landing:home')
    return redirect('landing:home')



def thanks_view(request):
    return render(request, 'landing/thankyou.html')