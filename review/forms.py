from django import forms
from . import models


class TicketForm(forms.ModelForm):
    class Meta:
        labels = {"title": "Titre", "description": "Description", "image": "Image"}
        model = models.Ticket
        fields = ("title", "description", "image")


class ReviewForm(forms.ModelForm):
    TicketForm()
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


class FollowUserForm(forms.Form):
    followed_user = forms.CharField(label=False, widget=forms.TextInput())
