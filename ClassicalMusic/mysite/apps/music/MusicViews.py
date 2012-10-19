from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson as json
from django.shortcuts import render, render_to_response, get_object_or_404, redirect

from music.models import *
from music.forms import *

import datetime
import string

class ComposersView(ListView):
    context_object_name = "composer_list"
    template_name="music/composers/index.html"
    paginate_by = 50

    def get_queryset(self):
        page = self.request.GET.get('page')
        startswith = self.request.GET.get('start')
        if startswith is None:
            startswith = 'A'
        composer_list = Composer.objects.filter(last_name__startswith=startswith).order_by('last_name')
        return composer_list

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ComposersView, self).get_context_data(**kwargs)
        allTheLetters = string.uppercase
        startswith = self.request.GET.get('start')
        if startswith is None:
            startswith = 'A'
        # Add in a QuerySet of alphabets
        context['alphabet'] = allTheLetters
        context['startswith'] = startswith
        return context

class CreateComposerView(CreateView):
    form_class=ComposerForm
    login_required=True
    template_name="music/composers/add.html"
    template_name_ajax = "music/composers/create_composer_ajax.html"
    template_name_ajax_success = "music/composers/create_composer_ajax_success.html"

    def get_template_names(self):
        if self.request.is_ajax():
            return [self.template_name_ajax]
        else:
            return [self.template_name]
    
    def form_valid(self, form):
        self.object = form.save()
        if self.request.is_ajax():
            data = {
                "status": "success",
                "location": self.object.get_absolute_url(),
                "html": render_to_string(self.template_name_ajax_success),
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            ctx = RequestContext(self.request, self.get_context_data(form=form))
            data = {
                "status": "failed",
                "html": render_to_string(self.template_name_ajax, ctx),
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return self.object.get_absolute_url()

class CompositionsView(ListView):
    context_object_name = "composition_list"
    template_name="music/compositions/index.html"
    paginate_by = 50

    def get_queryset(self):
        startswith = self.request.GET.get('start')
        if startswith is None:
            startswith = 'A'
        composition_list = Composition.objects.filter(title__startswith=startswith).order_by('title')
        return composition_list

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CompositionsView, self).get_context_data(**kwargs)
        allTheLetters = string.uppercase
        startswith = self.request.GET.get('start')
        if startswith is None:
            startswith = 'A'
        # Add in a QuerySet of alphabets
        context['alphabet'] = allTheLetters
        context['startswith'] = startswith
        return context

class CreateCompositionView(CreateView):
    form_class=CompositionForm
    login_required=True
    template_name="music/compositions/add.html"
    template_name_ajax = "music/compositions/create_ajax.html"
    template_name_ajax_success = "music/compositions/create_ajax_success.html"

    def get_template_names(self):
        if self.request.is_ajax():
            return [self.template_name_ajax]
        else:
            return [self.template_name]
    
    def form_valid(self, form):
        composition = form.save(commit=False)
        composer_id = self.kwargs.get('composer_id')
        if composer_id is not None:
            composition.composer = get_object_or_404(Composer, pk=composer_id)
        composition.save()
        self.object = composition
        if self.request.is_ajax():
            data = {
                "status": "success",
                "location": self.object.composer.get_absolute_url(),
                "html": render_to_string(self.template_name_ajax_success),
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            ctx = RequestContext(self.request, self.get_context_data(form=form))
            data = {
                "status": "failed",
                "html": render_to_string(self.template_name_ajax, ctx),
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        if self.success_url:
            return self.success_url

        composer_id = self.kwargs.get('composer_id')
        if composer_id is not None:
            return get_object_or_404(Composer, pk=composer_id).get_absolute_url()
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CreateCompositionView, self).get_context_data(**kwargs)
        composer_id = self.kwargs.get('composer_id')
        if composer_id is not None:
            context['composer'] = get_object_or_404(Composer, pk=composer_id)
        return context

class VideosView(ListView):
    context_object_name = "video_list"
    template_name="music/videos/list.html"
    paginate_by = 3

    def get_queryset(self):
        path = self.request.path
        video_list = Video.objects.filter(user=self.request.user)
        if path.endswith("ori/"):
            video_list = Video.objects.filter(user=self.request.user, original=True)

        if path.endswith("fav/"):
            video_list = Video.objects.filter(user=self.request.user, favorite=True)

        return video_list

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(VideosView, self).get_context_data(**kwargs)
        path = self.request.path
        if path.endswith("ori/"):
            context['type'] = 'ori'
        if path.endswith("fav/"):
            context['type'] = 'fav'
        return context

class CreateVideoView(CreateView):
    form_class=VideoForm
    login_required=True
    template_name="music/videos/add.html"
    template_name_ajax = "music/videos/create_ajax.html"
    template_name_ajax_success = "music/videos/create_ajax_success.html"

    def get_template_names(self):
        if self.request.is_ajax():
            return [self.template_name_ajax]
        else:
            return [self.template_name]

    def form_valid(self, form):
        video = form.save(commit=False)
        video.user = self.request.user
        path = self.request.path
        if path.endswith("ori/"):
            video.original=True
        if path.endswith("fav/"):
            video.favorite=True
        video.save()
        self.object = video
        if self.request.is_ajax():
            data = {
                "status": "success",
                "location": self.object.get_absolute_url(),
                "html": render_to_string(self.template_name_ajax_success),
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            ctx = RequestContext(self.request, self.get_context_data(form=form))
            data = {
                "status": "failed",
                "html": render_to_string(self.template_name_ajax, ctx),
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CreateVideoView, self).get_context_data(**kwargs)
        path = self.request.path
        if path.endswith("ori/"):
            context['type'] = 'ori'
        if path.endswith("fav/"):
            context['type'] = 'fav'
        return context

class EventsView(ListView):
    context_object_name = "event_list"
    template_name="music/events/list.html"
    paginate_by = 3

    def get_queryset(self):
        path = self.request.path
        event_list = Video.objects.filter(user=self.request.user)
        if path.endswith("past/"):
            event_list = Event.objects.filter(user=self.request.user, time__lte=datetime.datetime.now()).order_by('-time')
        if path.endswith("upcoming/"):
            event_list = Event.objects.filter(user=self.request.user, time__gte=datetime.datetime.now()).order_by('-time')
        return event_list

class CreateEventView(CreateView):
    form_class=EventForm
    login_required=True
    template_name="music/events/add.html"
    template_name_ajax = "music/events/create_ajax.html"
    template_name_ajax_success = "music/events/create_ajax_success.html"

    def get_template_names(self):
        if self.request.is_ajax():
            return [self.template_name_ajax]
        else:
            return [self.template_name]

    def form_valid(self, form):
        event = form.save(commit=False)
        event.user = self.request.user
        event.save()
        self.object = event
        if self.request.is_ajax():
            data = {
                "status": "success",
                "location": self.object.get_absolute_url(),
                "html": render_to_string(self.template_name_ajax_success),
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form):
        if self.request.is_ajax():
            ctx = RequestContext(self.request, self.get_context_data(form=form))
            data = {
                "status": "failed",
                "html": render_to_string(self.template_name_ajax, ctx),
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return self.object.get_absolute_url()

