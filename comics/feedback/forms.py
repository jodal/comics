from django import forms

class FeedbackForm(forms.Form):
    message = forms.CharField(label="What's on your heart",
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}))
