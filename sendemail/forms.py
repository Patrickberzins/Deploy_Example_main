# sendemail/forms.py
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import ContactsModel
from django.core.exceptions import ValidationError


class ContactsModelForm(ModelForm):
    class Meta:
        model = ContactsModel
        fields = ['from_email', 'repeat_email', 'subject', 'message']

    #To check if both emails are matching or not
    # and if not yet in DB    
    def clean(self):
        cleaned_data = super(ContactsModelForm, self).clean()
        email1 = self.cleaned_data.get('from_email')
        email2 = self.cleaned_data.get('repeat_email')
        print('From forms: ', email1,email2)
        if email1 != email2:
            raise forms.ValidationError('Emails do not match!')
        if email1 and User.objects.filter(email=email1).count():
            raise forms.ValidationError('This email is already in use! Try another email.')
            return email        


#Added April 27
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)
