from django.urls import path
from .views import home_view, waitlist_submit, feedback_submit

app_name = 'landing'

urlpatterns = [
    path('', home_view, name='home'),
    path('waitlist/', waitlist_submit, name='waitlist_submit'),
    path('feedback/', feedback_submit, name='feedback_submit'),
]