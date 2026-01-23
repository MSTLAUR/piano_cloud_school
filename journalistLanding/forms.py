from django import forms
from .models import EmailLeadJournalist


class WaitlistForm(forms.ModelForm):
    class Meta:
        model = EmailLeadJournalist
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email',
                'required': True,
                'class': 'waitlist-email-input'
            })
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = EmailLeadJournalist
        fields = ['email', 'feature', 'comment']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Your email address',
                'required': True,
                'class': 'feedback-email-input'
            }),
            'feature': forms.RadioSelect(),
            'comment': forms.Textarea(attrs={
                'placeholder': 'Tell us what feature would make your tutoring life easier...',
                'rows': 4
            })
        }
