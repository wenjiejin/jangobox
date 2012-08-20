from django.conf.urls.defaults import *

urlpatterns = patterns("music.views",
    url(r"^$", "composer_index"),

    url(r"^composers/$", "composer_index", name="composers"),
    url(r'^composers/(?P<composer_id>\d+)/$', 'composer_detail'),
    
    url(r"^compositions/$", "composition_index"),
    url(r'^compositions/(?P<composition_id>\d+)/$', 'composition_detail'),

    url(r"^repertoire/$", 'repertoire', name="repertoire"),
)
