from djongo import models
from django.contrib.auth.models import Permission, User
from django.core.validators import MaxValueValidator, MinValueValidator


class Movie(models.Model):

    _id = models.IntegerField(primary_key=True)
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    year = models.CharField(max_length=5)
    imdb_id = models.CharField(max_length=10)
    genre = models.CharField(max_length=100)
    movie_logo = models.CharField(max_length=300)
    imdb_rating = models.FloatField(validators=[MaxValueValidator(10), MinValueValidator(0)])
    release_date = models.CharField(max_length=100)
    summary = models.CharField(max_length=1000)

    def __str__(self):
        return self.title


class UserRating(models.Model):
    hashid = models.CharField(unique=True, max_length=200)
    user = models.CharField(max_length=100)
    movie = models.CharField(max_length=50)
    rating = models.FloatField(default=1, validators=[MaxValueValidator(5), MinValueValidator(0)])
