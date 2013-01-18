from django import template
import re
from bumble.bumbl.models import File
from bumble import settings

register = template.Library()

def filepaths(value):
    def dosub(match):
        f = File.objects.get(name=match.group(1))
        if f == None:
            return ""
        if settings.DEBUG:
            return "http://localhost:8000/" + settings.MEDIA_URL + f.f.name
        else:
            return settings.MEDIA_URL + f.f.name
    return re.sub(r'\{\{f:([^}]*)\}\}', dosub, value)

register.filter("filepaths", filepaths)

def urlify_path(path):
	if path == "":
		return ""
	return path[1:]

register.filter("urlify_path", urlify_path)
