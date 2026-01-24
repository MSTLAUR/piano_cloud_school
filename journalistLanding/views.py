from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .forms import WaitlistForm2, FeedbackForm
from .models import get_client_ip, get_location_from_ip, EmailLeadJournalist


def home_view(request):
    waitlist_form = WaitlistForm2()
    feedback_form = FeedbackForm()



    return render(request, 'journalistLanding/index.html')


def waitlist_submit2(request):
    if request.method == 'POST':
        form = WaitlistForm2(request.POST)
        if form.is_valid():
            # Get IP address and location data
            lead = form.save(commit=False)
            lead.ip_address = get_client_ip(request)
            location_data = get_location_from_ip(lead.ip_address)
            
            if location_data:
                lead.country = location_data.get('country')
                lead.city = location_data.get('city')
                lead.latitude = location_data.get('latitude')
                lead.longitude = location_data.get('longitude')
            
            lead.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Thanks for joining! We\'ll be in touch soon.'
                })
            else:
                messages.success(request, 'Thanks for joining! We\'ll be in touch soon.')
                return redirect('journalistLanding:home')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
            else:
                messages.error(request, 'Please check your email and try again.')
                return redirect('journalistLanding:home')
    return redirect('journalistLanding:home')


def feedback_submit(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Get IP address and location data
            lead = form.save(commit=False)
            lead.ip_address = get_client_ip(request)
            location_data = get_location_from_ip(lead.ip_address)

            if location_data:
                lead.country = location_data.get('country')
                lead.city = location_data.get('city')
                lead.latitude = location_data.get('latitude')
                lead.longitude = location_data.get('longitude')

            lead.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you for your feedback!'
                })
            else:
                messages.success(request, 'Thank you for your feedback!')
                return redirect('journalistLanding:home')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
            else:
                messages.error(request, 'Please complete the form and try again.')
                return redirect('journalistLanding:home')
    return redirect('journalistLanding:home')
