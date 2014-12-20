from django import template
import re
from bumble.bumbl.models import File
from bumble import settings
import markdown

register = template.Library()

def filepaths(value):
    def dosub(match):
        try:
            f = File.objects.get(name=match.group(1))
        except File.DoesNotExist:
            return ""
        if f == None:
            return ""
        else:
            return settings.MEDIA_URL + f.f.name
    return re.sub(r'\{\{f:([^}]*)\}\}', dosub, value)

register.filter("filepaths", filepaths)

def md(value):
    def dosub(match):
        return markdown.markdown(match.group(1))
    return re.sub(r'\*\*\*(([^*]|(\*[^*])|(\*\*[^*]))*)\*\*\*', dosub, value)

register.filter("md", md)

def urlify_path(path):
	if path == "":
		return ""
	return path[1:]

register.filter("urlify_path", urlify_path)

def ensure_trailing_slash(path):
    if not path.endswith("/"):
        return path + "/"
    else:
        return path

register.filter("ensure_trailing_slash", ensure_trailing_slash)

def thumb(text):
    text = md(filepaths(text))
    match = re.search("img src=\"([^\"]+)\"", text)
    if match:
        return match.group(1)
    else:
        return None

register.filter("thumb", thumb)
