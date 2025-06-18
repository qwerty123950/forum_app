from django import forms
from .models import Board, Topic, Post

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'description']


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your message here'}),
        max_length=4000,
        help_text='The max length of the text is 4000.'
    )

    class Meta:
        model = Topic
        fields = ['subject']

