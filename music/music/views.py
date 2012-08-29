from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from music.models import Event, Composer, Composition, Repertoire, Video
import datetime
import string

def composer_index(request):
    allTheLetters = string.uppercase
    composer_list = Composer.objects.all().order_by('last_name')
    return render_to_response('music/composers/index.html',
                               {'composer_list': composer_list,
                                'alphabet' : allTheLetters,
                                'startswith' : 'A'},
                                context_instance=RequestContext(request))

def composer_startswith(request, startswith):
    allTheLetters = string.uppercase
    composer_list = Composer.objects.filter(last_name__startswith=startswith).order_by('last_name')
    return render_to_response('music/composers/index.html',
                               {'composer_list': composer_list,
                                'alphabet' : allTheLetters,
                                'startswith' : startswith},
                                context_instance=RequestContext(request))
# ...
def composer_detail(request, composer_id):
    composer = get_object_or_404(Composer, pk=composer_id)
    return render_to_response('music/composers/detail.html', {'composer': composer},context_instance=RequestContext(request))

def composition_index(request):
    composition_list = Composition.objects.all().order_by('-title')[:5]
    return render_to_response('music/compositions/index.html', {'composition_list': composition_list},context_instance=RequestContext(request))
# ...
def composition_detail(request, composition_id):
    composition = get_object_or_404(Composition, pk=composition_id)
    return render_to_response('music/compositions/detail.html', {'composition': composition}, context_instance=RequestContext(request))
# ...
def repertoire(request):
    if request.user.is_authenticated():
        repertoire_reserved_list = Repertoire.objects.filter(user=request.user, reserved=True)
        repertoire_practicing_list = Repertoire.objects.filter(user=request.user, practicing=True)
        ori_video_list = Video.objects.filter(user=request.user, original=True)
        fav_video_list = Video.objects.filter(user=request.user, favorite=True)
        upcoming_event_list = Event.objects.filter(user=request.user, time__gte=datetime.datetime.now())
        past_event_list = Event.objects.filter(user=request.user, time__lte=datetime.datetime.now())

        return render_to_response('music/repertoires/repertoire.html',
                                  {'repertoire_reserved_list': repertoire_reserved_list,
                                   'repertoire_practicing_list': repertoire_practicing_list,
                                   'ori_video_list': ori_video_list,
                                   'fav_video_list': fav_video_list,
                                   'upcoming_event_list': upcoming_event_list,
                                   'past_event_list': past_event_list},
                                   context_instance=RequestContext(request))
    else:
        return redirect('/account/login/')

def event_index(request):
    if request.user.is_authenticated():
        event_list = Event.objects.all().order_by('-time')
        return render_to_response('music/events/index.html', {'event_list': event_list},context_instance=RequestContext(request))
    else:
        return redirect('/account/login/')

def event_detail(request, event_id):
    if request.user.is_authenticated():
        event = get_object_or_404(Event, pk=event_id)
        return render_to_response('music/events/detail.html', {'event': event}, context_instance=RequestContext(request))
    else:
        return redirect('/account/login/')

def video_index(request):
    if request.user.is_authenticated():
        ori_video_list = Video.objects.filter(user=request.user, original=True)
        fav_video_list = Video.objects.filter(user=request.user, favorite=True)
        return render_to_response('music/videos/index.html',
                                  {'ori_video_list': ori_video_list,
                                   'fav_video_list': fav_video_list},
                                   context_instance=RequestContext(request))
    else:
        return redirect('/account/login/')
