from django import forms
from django.forms import ModelForm
from bumble.bumbl.models import Comment

class CommentForm(ModelForm):
    text = forms.CharField(max_length=5000, widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ["commenter", "email", "text"]

