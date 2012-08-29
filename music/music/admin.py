from django.contrib import admin

from music.models import *

class CompositionInline(admin.StackedInline):
    model = Composition
    extra = 3

class ComposerAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Biography',{'fields': ['first_name', 'last_name', 'picture']}),
        ('Detailed', {'fields': ['description'], 'classes': ['collapse']}),
    ]
    inlines = [CompositionInline]
    list_filter = ['first_name', 'last_name']
    search_fields = ['first_name', 'last_name']

admin.site.register(Composer, ComposerAdmin)
admin.site.register(Composition)
admin.site.register(Repertoire)
admin.site.register(Score)
admin.site.register(Event)
admin.site.register(Video)