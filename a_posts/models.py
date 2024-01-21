import ckeditor.fields
from django.db import models
import uuid
from xml.etree import ElementTree
from django.contrib.auth.models import User
from PIL import Image
from django.core.exceptions import ValidationError
# Create your models here.
from django.utils.html import strip_tags
from bleach import clean
from ckeditor.fields import RichTextField
from django.db import models
from PIL import Image
from django.templatetags.static import static
from django_resized import ResizedImageField
def strip_tags_except_allowed(value, allowed_tags):
    """
    Strip HTML tags from the given value, except for the allowed_tags.
    """
    return clean(value, tags=allowed_tags, strip=True)

class ValidXHTMLTextField(models.TextField):
    def validate_xhtml(self, value):
        try:
            stripped_value = strip_tags_except_allowed(value, allowed_tags=['a', 'code', 'i', 'strong'])
            if stripped_value != value:
                raise ValidationError('Недопустимые HTML теги.')
            # Проверка на валидность XHTML
            ElementTree.fromstring(f'<root>{value}</root>')
        except ElementTree.ParseError:
            raise ValidationError('Неверный формат XHTML.')

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        self.validate_xhtml(value)




class Post(models.Model):
    
    
    title = models.CharField(max_length=500)
    artist = models.CharField(max_length=500, null=True)
    # url = models.URLField(max_length=500, null=True, blank=True)
    # image = models.URLField(max_length=500, null=True, blank=True)
    photo_field = ResizedImageField(size=[320, 240], quality=85, upload_to='images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL , null=True, related_name='posts')
    body = models.TextField()
    tags = models.ManyToManyField('Tag')
    text_file = models.FileField(upload_to='files/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    # uuiu - it's uniwersally unique identifier(uuid)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    email = models.EmailField()
    likes = models.ManyToManyField(User, related_name='likedposts', through="LikedPost")
    text = RichTextField(verbose_name='Text Message')
    
    def __str__(self):
        return str(self.title)
    
    class Meta:
        ordering = ['-created']
    
    @property
    def photo(self):
        try:
            photo = self.photo_field.url
        except:
            photo = static('images/avatar_default.svg')
        return photo
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     if self.photo_field:
    #         # Open the image file
    #         img = Image.open(self.photo_field.path)

    #         # Set the desired size
    #         target_size = (320, 240)

    #         # Resize the image only if it's in an acceptable format
    #         allowed_formats = ['JPEG', 'PNG', 'GIF']
    #         if img.format.upper() in allowed_formats:
    #             img.thumbnail(target_size)
    #             img.save(self.photo_field.path)
    #         else:
    #             # Handle unsupported format (you may want to raise an exception or log a message)
    #             pass
    
    
class LikedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)    
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} : {self.post.title}'

    
class Tag(models.Model):
    name = models.CharField(max_length=20)
    image = models.FileField(upload_to='icons/', null=True, blank=True)
    slug = models.SlugField(max_length=20, unique=True)
    order = models.IntegerField(null=True)
    
    
    def __str__(self):
        return self.name 
    
    class Meta:
        ordering = ['order']
        
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')
    parent_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(User, related_name='likedcomments', through='LikedComment')
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key = True, editable=False)

    def __str__(self):
        try:
            return f'{self.author.username} : {self.body[:30]}' 
        except:
            return f'no author : {self.body[:30]}' 
        
    class Meta:
        ordering = ['-created']
        
        
class LikedComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)    
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} : {self.comment.body[:30]}'


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="replies")
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies", null=True, blank=True)
    parent_reply = models.ForeignKey('Reply', on_delete=models.CASCADE, related_name="replies", null=True, blank=True)
    level = models.IntegerField(default=1)
    body = models.CharField(max_length=150)
    likes = models.ManyToManyField(User, related_name='likedreplies', through='LikedReply')
    created = models.DateTimeField(auto_now_add=True)
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key = True, editable=False)

    def __str__(self):
        try:
            return f'{self.author.username} : {self.body[:30]}'
        except:
            return f'no author : {self.body[:30]}'

    class Meta:
        ordering = ['created']
        
        
class LikedReply(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)    
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.user.username} : {self.reply.body[:30]}'