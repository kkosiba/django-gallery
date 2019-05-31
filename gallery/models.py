import random
from django.db import models
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager


# Create your models here.
class Album(models.Model):
    name = models.CharField(max_length=100, unique=True)
    creation_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Albums"
        ordering = ("-creation_date",)

    def item_count(self):
        n = Picture.objects.filter(album__name=self.name).count()
        if n > 1:
            return f"{n} items."
        elif n == 1:
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
        return reverse("gallery:single_album", kwargs={"album_name": self.name})


class Picture(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="pictures")
    picture = models.ImageField(upload_to="media", default="media/None/no-img.jpg")
    description = models.CharField(max_length=500, default="Empty")

    # tags mechanism
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "gallery:single_picture",
            kwargs={"album_name": self.album.name, "pk": self.pk},
        )
