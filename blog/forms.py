from django import forms
from .models import *
from ckeditor.widgets import CKEditorWidget

from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Blog

class BlogForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), required=False)

    class Meta:
        model = Blog
        fields = ['title', 'author', 'author_designation', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Blog Title'
        })
        self.fields['author'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Author Name'
        })
        self.fields['author_designation'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Author Designation'
        })
        self.fields['image'].widget.attrs.update({
            'class': 'form-control'
        })

