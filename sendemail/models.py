from django.db import models
from django.forms import ModelForm

# Create your models here.

class ContactsModel(models.Model):
    from_email = models.EmailField()
    repeat_email = models.EmailField()
    subject = models.CharField(max_length=1024)
    message = models.TextField(max_length=1024*2) 
    def __unicode__(self):
        return self.name
    def clean_email(self):
        if User.objects.filter(from_email = from_email).exists():
            raise forms.ValidationError("Email already exists")

