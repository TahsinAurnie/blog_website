from django import forms
from .models import Blog
from ckeditor.fields import RichTextField

class TextForm(forms.Form):
    text = forms.CharField(required=True, widget=forms.Textarea)

class AddBlogForm(forms.ModelForm):
    description = RichTextField()
    class Meta:
        model = Blog
        fields = ("title", "category", "banner", "description")