from django.conf.urls.defaults import *

urlpatterns = patterns("music.views",
    url(r"^$", "composer_index"),

    url(r"^composers/$", "composer_index", name="composers"),
    url(r'^composers/(?P<startswith>\D+)/$', 'composer_startswith'),
    url(r'^composers/(?P<composer_id>\d+)/$', 'composer_detail'),

    url(r"^compositions/$", "composition_index", name="compositions"),
    url(r'^compositions/(?P<composition_id>\d+)/$', 'composition_detail'),

    url(r"^repertoire/$", 'repertoire', name="repertoire"),

    url(r"^events/$", "event_index", name="events"),
    url(r'^events/(?P<event_id>\d+)/$', 'event_detail'),

    url(r"^videos/$", "video_index", name="videos"),
)
