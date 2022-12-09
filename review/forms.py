from django.contrib.auth import get_user_model
from django import forms
from . import models


class TicketForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        labels = {
            "title": "Titre",
            "description": "Description",
            "image": "Image"}
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
        widgets = {
            "rating": forms.RadioSelect(
                choices=CHOICES),
            "body": forms.Textarea}


class SubsForm(forms.ModelForm):
    followed_user = forms.CharField(
        max_length=100,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"}),
    )

    class Meta:
        model = models.UserFollows
        fields = ["followed_user"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean_followed_user(self):
        user_model = get_user_model()
        follows = models.UserFollows.objects.select_related(
            "followed_user").filter(user=self.user)
        if self.user.username == self.cleaned_data["followed_user"]:
            raise forms.ValidationError(
                "Vous ne pouvez pas vous abonner à vous-même")
        elif self.cleaned_data["followed_user"] in [
            follow.followed_user.username for follow in follows
        ]:
            raise forms.ValidationError(
                "Vous êtes déjà abonné a cet utilisateur")
        try:
            return user_model.objects.get(
                username=self.cleaned_data["followed_user"])
        except user_model.DoesNotExist:
            raise forms.ValidationError("Cet utilisateur n'existe pas")
