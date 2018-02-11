from .models import Entry, Tag, File, Comment, Redirect, RawEntry
from django.contrib import admin

class EntryAdmin(admin.ModelAdmin):
    exclude = ("path", "total_css", "total_section_content", )

admin.site.register(Entry, EntryAdmin)
admin.site.register(Tag)
admin.site.register(File)
admin.site.register(Comment)
admin.site.register(Redirect)
admin.site.register(RawEntry)
