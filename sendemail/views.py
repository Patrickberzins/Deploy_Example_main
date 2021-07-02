# sendemail/views.py
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import ContactsModel
from .forms import ContactsModelForm

from django.urls import reverse
from .forms import CustomUserCreationForm
from django.contrib.auth import login

def validateEmail( email ):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False

            
def contactView(request):
    if request.method == 'GET':
        form = ContactsModelForm()
    elif request.method == 'POST':
        form = ContactsModelForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            validateEmail(from_email)
            repeat_email = form.cleaned_data['repeat_email']
            validateEmail(repeat_email)
            message = form.cleaned_data['message']
            u = form.save()
            print({'form': form})

            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    else:
        form_class = ContactsModelForm
    
    return render(request, "email.html", {'form': form})

def successView(request):
    return HttpResponse('Success! Thank you for your message.')

#Added April 27

def dashboard(request):
    return render(request, "dashboard.html")

def register(request):
    if request.method == "GET":
        return render(
            request, "register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("dashboard"))