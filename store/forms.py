from django import forms
from .models import ReviewRating

class ReviewForm(forms.ModelForm):
    class Meta:
        models = ReviewRating
        field = ['subject', 'review', 'rating']