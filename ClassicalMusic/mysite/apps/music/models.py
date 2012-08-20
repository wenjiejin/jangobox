from django.db import models
from django.contrib.auth.models import User

class Composer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    picture = models.FileField(upload_to='composer')
    description = models.TextField()
    # ...
    def __unicode__(self):
        return self.last_name + ', ' + self.first_name

class Composition(models.Model):
    composer = models.ForeignKey(Composer)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    year = models.CharField(max_length=20)
    first_performance = models.CharField(max_length=200)
    publication = models.TextField()
    average_duration = models.CharField(max_length=200)
    Instrumentation = models.TextField()
    key = models.CharField(max_length=200)
    opus_catalogue_number = models.CharField(max_length=200)

    # ...
    def __unicode__(self):
        return self.title + ', by ' + self.composer.last_name

class Score(models.Model):
    composition = models.ForeignKey(Composition)
    editor = models.CharField(max_length=200)
    copyright = models.CharField(max_length=200)
    publisher = models.TextField()
    score = models.FileField(upload_to='score')

    # ...
    def __unicode__(self):
        return self.composition.title + ', by ' + self.publisher

class Repertoire(models.Model):
    user = models.ForeignKey(User)
    piece = models.ForeignKey(Composition)
    reserved = models.BooleanField()
    practicing = models.BooleanField()
    # ...
    def __unicode__(self):
        return self.piece.title

class Event(models.Model):
    user = models.ForeignKey(User)
    title = models.TextField()
    time = models.DateTimeField()
    location = models.TextField()
    description = models.TextField()
    invitation = models.TextField()

    # ...
    def __unicode__(self):
        return self.title

class Video(models.Model):
    user = models.ForeignKey(User)
    embeded = models.TextField()
    original = models.BooleanField()
    favorite = models.BooleanField()

    # ...
    def __unicode__(self):
        return self.embeded