from .models import Comment, Post
from django import forms  #django has two base classes to build form 1. Form and 2. ModelForm

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('title', 'body', 'status',  'tags')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'body': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'})

        }

    


            
