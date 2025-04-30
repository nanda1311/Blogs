from django.db import models
from tinymce.models import HTMLField
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class Blog(models.Model):
     title = models.CharField(max_length=250)
     author = models.CharField(max_length=250)
     author_designation = models.CharField(max_length=250)
     description = RichTextField()
     image = models.ImageField()
     created_at = models.DateTimeField(auto_now=True)
     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
     slug = models.SlugField(null=True, blank=True)


     def __str__(self):
          return self.title
     


     def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            original_slug = self.slug
            counter = 1
            while Blog.objects.filter(slug=self.slug).exists():
                self.slug = f'{original_slug}-{counter}'
                counter += 1
        super().save(*args, **kwargs)



     