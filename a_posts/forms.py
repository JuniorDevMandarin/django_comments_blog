from django.forms import widgets, ModelForm
from django import forms
from .models import *
from captcha.fields import CaptchaField
from ckeditor.fields import RichTextField

class PostCreateForm(ModelForm):
    captcha = CaptchaField()
    paragragh=RichTextField()
    italic = RichTextField()
    link = RichTextField()
    strong = RichTextField()
    class Meta:
        model = Post
        fields = [ 'title', 'text', 'email', 'text_file', 'author', 'tags',  'photo_field']
        labels = {
            'body' : 'Caption',
            'tags' : 'Category'
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3,
                                          'placeholder': 'Add a text...',
                                          'class': 'font1 text-4xl'}),
          
            'tags': forms.CheckboxSelectMultiple(),
        }


class PostEditForm(ModelForm):

    paragragh=RichTextField()
    italic = RichTextField()
    link = RichTextField()
    strong = RichTextField()
    class Meta:
        model = Post
        fields = ['text', 'tags']
        labels = {
            'text': '',
            'tags': 'Category'
        }
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3,
                                   'class': 'font1 text-4xl'}),
            'tags': forms.CheckboxSelectMultiple(),
        }
        
class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={'placeholder': 'Add comment...'})
        }
        labels = {
            'body': ''
        }
        
class ReplyCreateForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['body']
        widgets = {
            'body' : forms.TextInput(attrs={'placeholder': 'Add reply ...', 'class': "!text-sm"})
        }
        labels = {
            'body': ''
        }
        
class NestedReplyCreateForm(ModelForm):
    class Meta:
        model = Reply
        fields = ['body']
        widgets = {
            'body' : forms.TextInput(attrs={'autofocus': True, 'class': "!text-sm bg-gray-200 !p-0 !pl-2 !h-8"})
        }
        labels = {
            'body': ''
        }