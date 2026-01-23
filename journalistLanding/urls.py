from django.urls import path
from .views import home_view, waitlist_submit, feedback_submit

app_name = 'journalistLanding'

urlpatterns = [
    path('jl/', home_view, name='home'),
    path('jl/waitlist/', waitlist_submit, name='waitlist_submit'),
    path('jl/feedback/', feedback_submit, name='feedback_submit'),
]
