from django.conf.urls.defaults import *
from django.views.generic import ListView

from music.models import Event, Composer, Composition, Repertoire, Video
from music.MusicViews import *

urlpatterns = patterns("music.views",
    url(r"^$", ComposersView.as_view(), name="composers"),

    url(r"^composers/$", ComposersView.as_view(), name="composers"),
#    url(r'^composers/(?P<startswith>\D+)/$', 'composer_startswith'),
    url(r'^composers/start(?P<startswith>\D+)&page(?P<page>[0-9]+)/$', ComposersView.as_view()),
    url(r'^composers/start(?P<startswith>\D+)/$', ComposersView.as_view()),

    url(r'^composers/(?P<composer_id>\d+)/$', 'composer_detail', name="composer_detail"),
    url(r"^composers/add/$", CreateComposerView.as_view(), name="composer_add"),

    url(r"^compositions/$", CompositionsView.as_view(), name="compositions"),
#    url(r"^compositions/$", "composition_index", name="compositions"),
    url(r'^compositions/(?P<composition_id>\d+)/$', 'composition_detail'),
    url(r"^compositions/add/$", CreateCompositionView.as_view(), name="composition_add"),
    url(r"^compositions/add/(?P<composer_id>\d+)/$", CreateCompositionView.as_view(), name="composition_add_to_composer"),
    url(r'^compositions/practice/(?P<composition_id>\d+)/$', 'composition_practice', name="composition_practice"),
    url(r'^compositions/like/(?P<composition_id>\d+)/$', 'composition_like', name="composition_like"),

    url(r"^repertoire/$", 'repertoire', name="repertoire"),

    url(r"^events/$", "event_index", name="events"),
    url(r"^events/(?P<type>past|upcoming)/$", EventsView.as_view(), name="event_list"),
    url(r"^events/add/$", CreateEventView.as_view(), name="event_add"),
    url(r'^events/(?P<event_id>\d+)/$', 'event_detail'),

    url(r"^videos/$", "video_index", name="videos"),
    url(r"^videos/(?P<type>ori|fav)/$", VideosView.as_view(), name="video_list"),
#    url(r"^videos/type(?P<type>ori|fav)&page(?P<page>[0-9]+)/$", VideosView.as_view(), name="video_list"),
    url(r"^videos/add/(?P<type>ori|fav)/$", CreateVideoView.as_view(), name="video_add"),


)
