from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

import re

class Composer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    picture = models.FileField(upload_to='composer', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    # ...
    def __unicode__(self):
        return self.last_name + ', ' + self.first_name

    def get_absolute_url(self):
        kwargs = {"composer_id": self.pk}
        return reverse("composer_detail", kwargs=kwargs)

class Composition(models.Model):
    composer = models.ForeignKey(Composer)
    album_photo = models.FileField(upload_to='composition', null=True, blank=True)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    year = models.CharField(max_length=20)
    first_performance = models.CharField(max_length=200, null=True, blank=True)
    publication = models.TextField(null=True, blank=True)
    average_duration = models.CharField(max_length=200, null=True, blank=True)
    Instrumentation = models.TextField()
    key = models.CharField(max_length=200, null=True, blank=True)
    opus_catalogue_number = models.CharField(max_length=200, null=True, blank=True)

    # ...
    def __unicode__(self):
        return self.title + ', by ' + self.composer.last_name

    def get_absolute_url(self):
        kwargs = {"composition_id": self.pk}
        return reverse("composition_detail", kwargs=kwargs)

class Score(models.Model):
    composition = models.ForeignKey(Composition)
    editor = models.CharField(max_length=200, null=True, blank=True)
    copyright = models.CharField(max_length=200, null=True, blank=True)
    publisher = models.TextField(null=True, blank=True)
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
    title = models.TextField(null=True, blank=True)
    time = models.DateTimeField()
    location = models.TextField(null=True, blank=True)
    description = models.TextField()
    invitation = models.TextField(null=True, blank=True)

    # ...
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        kwargs = {}
        return reverse("events", kwargs=kwargs)

class Video(models.Model):
    user = models.ForeignKey(User)
    title = models.TextField(null=True, blank=True)
    embeded = models.TextField()
    original = models.BooleanField()
    favorite = models.BooleanField()

    def normalizeEmbeded(self):
        embeded = re.sub(r'width=.*?[\s$]', "width=\"200\" ", self.embeded)
        embeded = re.sub(r'height=.*?[\s$]', "height=\"150\" ", embeded)
        return embeded
    # ...
    def __unicode__(self):
        return self.embeded

    def get_absolute_url(self):
        kwargs = {}
        return reverse("videos", kwargs=kwargs)
