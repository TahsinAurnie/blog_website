from django.db import models
from user_profile.models import User
from django.utils.text import slugify
from .slugs import generate_unique_slug
from ckeditor.fields import RichTextField

# Create your models here.
class Category(models.Model):
    class Meta:
        verbose_name_plural = 'categories'
        verbose_name = 'category'
        ordering = ['title']
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    def save(self,*args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
class Tag(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
    def save(self,*args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
class Blog(models.Model):
    user = models.ForeignKey(User, related_name= 'user_blogs', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name= 'category_blogs', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, related_name= 'tag_blogs', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=150)
    description = RichTextField()
    slug = models.SlugField(max_length=100, blank=True, null=True)
    banner = models.ImageField(upload_to="blog_banners")
    likes = models.ManyToManyField(User, related_name= 'user_likes', blank=True)

    def __str__(self):
        return self.title
    def save(self,*args, **kwargs):
        updating = self.pk is not None
        if updating:
            self.slug = generate_unique_slug(self, self.title, update=True)
            super().save(*args, **kwargs)
            # self.slug = slugify(self.title)
        else:
            self.slug = generate_unique_slug(self, self.title)
            super().save(*args, **kwargs)

class Comment(models.Model):
    user = models.ForeignKey(User, related_name="user_comment", on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, related_name="blog_comment", on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    
class Reply(models.Model):
    class Meta:
        verbose_name_plural = 'replies'
        verbose_name = 'reply'
    user = models.ForeignKey(User, related_name="user_replies", on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name="comment_replies", on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.text



