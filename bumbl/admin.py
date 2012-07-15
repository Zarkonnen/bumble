from bumble.bumbl.models import Entry, Tag, File
from django.contrib import admin

class EntryAdmin(admin.ModelAdmin):
    exclude = ("path", )

admin.site.register(Entry, EntryAdmin)
admin.site.register(Tag)
admin.site.register(File)
