from django import forms
from .models import EmailLeadJournalist


class WaitlistForm2(forms.ModelForm):
    class Meta:
        model = EmailLeadJournalist
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'input',
                'placeholder': 'you@email.com'
            })
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = EmailLeadJournalist
        fields = ['email', 'first_name', 'feature', 'comment']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'input',
                'placeholder': 'your@email.com'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Your name'
            }),
            'feature': forms.Select(attrs={
                'class': 'input'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'input',
                'placeholder': 'Tell us what you think...',
                'rows': 4
            })
        }
