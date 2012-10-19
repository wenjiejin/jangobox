from django.forms import ModelForm, SplitDateTimeWidget

from music.models import Event, Composer, Composition, Video
from music.fields import JqSplitDateTimeField
from music.widgets import JqSplitDateTimeWidget

class ComposerForm(ModelForm):
    class Meta:
        model = Composer
        exclude = ('picture',)

class CompositionForm(ModelForm):
    class Meta:
        model = Composition
        exclude = ('composer', 'album_photo', 'first_performance','publication', 'Instrumentation', 'opus_catalogue_number',)

class EventForm(ModelForm):
    time = JqSplitDateTimeField(label='time', widget=JqSplitDateTimeWidget(attrs={'date_class':'datepicker','time_class':'timepicker'}))

    class Meta:
        model = Event
        fields = ('time', 'description')

class VideoForm(ModelForm):
    class Meta:
        model = Video
        exclude = ('user', 'title', 'original', 'favorite')

