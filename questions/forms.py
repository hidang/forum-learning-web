from django import forms
from . import models


class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ['title', 'content', 'tag', 'thumbnail']


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['content']
