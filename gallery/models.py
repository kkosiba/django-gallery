from django.db import models

from django.utils import timezone
from django.urls import reverse

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# tags
from taggit.managers import TaggableManager

import random

# Create your models here.
class Album(models.Model):
    name = models.CharField(max_length=100, unique=True)
    creation_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = 'Albums'
        ordering = ('-creation_date', )

    def item_count(self):
        n = Picture.objects.filter(album__name=self.name).count()
        if n>1:
            return f"{n} items."
        elif n==1:
            return "1 item."
        return "Empty album."

    def random_image(self):
        lst = Picture.objects.filter(album__name=self.name)
        if lst:
            return random.choice(lst).picture
        return None

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('gallery:single_album', kwargs={'album_name': self.name})


class Picture(models.Model):
    album = models.ManyToManyField(Album, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pictures')
    picture = models.ImageField(upload_to='media', default='media/None/no-img.jpg')
    title = models.CharField(max_length=300)
    published_date = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=500, default='Empty')

    # tags mechanism
    tags = TaggableManager()
    
    class Meta:
        ordering = ('-published_date', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('gallery:single_picture', kwargs={'pk': self.pk})
