from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    genres = models.ManyToManyField('Genre', related_name='movies')
    poster_image = models.ImageField(upload_to='posters/')
    duration = models.IntegerField(help_text="Duration in minutes")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name