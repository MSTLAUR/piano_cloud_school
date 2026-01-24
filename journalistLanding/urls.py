from django.urls import path
from .views import home_view, waitlist_submit2, feedback_submit

app_name = 'journalistLanding'

urlpatterns = [
    path('jl/', home_view, name='home'),
    path('jl/waitlist/', waitlist_submit2, name='waitlist_submit2'),
    path('jl/feedback/', feedback_submit, name='feedback_submit'),
]
