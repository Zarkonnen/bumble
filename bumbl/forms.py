from django import forms
from django.forms import ModelForm
from bumble.bumbl.models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["commenter", "email", "text"]

