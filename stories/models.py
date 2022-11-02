from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
import datetime

from matplotlib import image
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length= 150, unique= True)
    def __str__(self):
        return self.name

class Stories(models.Model):
    Category = models.ForeignKey(Category, on_delete= models.PROTECT)
    name = models.CharField(max_length= 250, unique= True)
    author = models.CharField(max_length= 250)
    url = models.URLField(unique = True)
    url_video = models.TextField(null = True, blank = True)
    content = models.TextField()
    summary = models.TextField(null = True, blank = True)
    content = RichTextUploadingField(blank = True)
    # viewed = models.IntegerField(null = True, blank = True, default = 0)
    public_day = models.DateField(default = timezone.now)
    image = models.ImageField(upload_to = 'stories/images', default = 'stories/image/logo.jpg')
    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length= 300)
    email = models.EmailField(null = True)
    subject = models.CharField(max_length= 400, null = True)
    message = models.TextField(null = True)

    def __str__(self):
        return self.name

