from django.db import models

from django.utils import timezone

from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'name': self.name})


class Picture(models.Model):
    category = models.ManyToManyField(Category, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pictures')
    picture = models.ImageField(upload_to='media', default='media/None/no-img.jpg')
    title = models.CharField(max_length=300)
    published_date = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=500, default='Empty')

    class Meta:
        ordering = ('-published_date', )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('single_picture', kwargs={'pk': self.pk})
