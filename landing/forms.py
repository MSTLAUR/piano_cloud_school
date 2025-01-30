from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit
from .models import Email_lead_models

class Email_lead_Form(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)

    def __init__(self, *args, **kwargs):
        super(Email_lead_Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
        
        
        
class AdminCreationForm(forms.ModelForm):

    
    
    class Meta:
        model = Email_lead_models
        fields = ('email', 'name')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))