import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Booking


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class BookingForm(forms.ModelForm):
    SERVICE_CHOICES = [
        ("Consultation", "Consultation"),
        ("Document Service", "Document Service"),
        ("Technical Support", "Technical Support"),
        ("Payment Counter", "Payment Counter"),
        ("General Enquiry", "General Enquiry"),
    ]

    TIME_CHOICES = [
        ("09:00", "09:00 AM"),
        ("10:00", "10:00 AM"),
        ("11:00", "11:00 AM"),
        ("12:00", "12:00 PM"),
        ("14:00", "02:00 PM"),
        ("15:00", "03:00 PM"),
        ("16:00", "04:00 PM"),
        ("17:00", "05:00 PM"),
    ]

    service = forms.ChoiceField(choices=SERVICE_CHOICES)
    time_slot = forms.ChoiceField(choices=TIME_CHOICES)

    class Meta:
        model = Booking
        fields = ("service", "date", "time_slot")
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_date(self):
        date = self.cleaned_data["date"]
        if date < datetime.date.today():
            raise ValidationError("Booking date cannot be in the past.")
        return date

    def clean(self):
        cleaned = super().clean()
        service = cleaned.get("service")
        time_slot = cleaned.get("time_slot")

        valid_services = [c[0] for c in self.SERVICE_CHOICES]
        valid_times = [t[0] for t in self.TIME_CHOICES]

        if service and service not in valid_services:
            raise ValidationError("Invalid service selected.")

        if time_slot and time_slot not in valid_times:
            raise ValidationError("Invalid time slot selected.")

        return cleaned
