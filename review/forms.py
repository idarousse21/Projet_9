from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . import models


class TicketForm(forms.ModelForm):
    class Meta:
        labels = {"title": "Titre", "description": "Description", "image": "Image"}
        model = models.Ticket
        fields = ("title", "description", "image")


class ReviewForm(forms.ModelForm):
    class Meta:
        labels = {"headline": "Titre", "rating": "Note", "body": "Commentaire"}
        CHOICES = [
            ("1", 1),
            ("2", 2),
            ("3", 3),
            ("4", 4),
            ("5", 5),
        ]
        model = models.Review
        fields = ("headline", "rating", "body")
        widgets = {"rating": forms.RadioSelect(choices=CHOICES)}


class SubsForm(forms.ModelForm):
    class Meta:
        model = models.UserFollows
        fields = ["followed_user"]
