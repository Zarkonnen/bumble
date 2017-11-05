from django import forms
from django.forms import ModelForm
from bumble.bumbl.models import Comment

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["commenter", "email", "text"]
        widgets = {
            'commenter': forms.TextInput(attrs={'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'text': forms.Textarea(attrs={'placeholder': 'Comment'})
        }

