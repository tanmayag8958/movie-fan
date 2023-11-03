from django.db import models

from movie_fan.models import TimeStampedModel


class Genre(models.Model):
    name = models.CharField(max_length=100, primary_key=True)

    class Meta:
        app_label = 'dashboard'


class Star(TimeStampedModel):
    # Currently assuming each star have a unique name as we don't have
    # more information about stars to uniquely identify them
    name = models.CharField(max_length=200, primary_key=True)

    class Meta:
        app_label = 'dashboard'


class Director(TimeStampedModel):
    # Currently assuming each director have a unique name as we don't have
    # more information about stars to uniquely identify them
    name = models.CharField(max_length=200, primary_key=True)

    class Meta:
        app_label = 'dashboard'


class Media(TimeStampedModel):
    name = models.CharField(max_length=200, null=False)
    run_time = models.IntegerField(null=True)
    rating = models.FloatField(null=False, default=0)
    votes = models.IntegerField(null=False, default=0)
    description = models.TextField(null=True)
    genres = models.ManyToManyField(to=Genre)
    stars = models.ManyToManyField(to=Star)
    directors = models.ManyToManyField(to=Director)

    class Meta:
        app_label = 'dashboard'


class Movie(TimeStampedModel):
    media = models.ForeignKey(to=Media, on_delete=models.CASCADE)
    year = models.CharField(max_length=10, null=True)

    class Meta:
        app_label = 'dashboard'
        unique_together = ['media', 'year']


class Series(TimeStampedModel):
    media = models.ForeignKey(to=Media, on_delete=models.CASCADE)
    start_year = models.CharField(max_length=10, null=True)
    end_year = models.CharField(max_length=10, null=True)

    class Meta:
        app_label = 'dashboard'
        unique_together = ['media', 'start_year']
