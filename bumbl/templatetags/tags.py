from django import template
from django.core.urlresolvers import reverse
import re
from ..models import File, Tag
from django.conf import settings
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

def tagslist(value):
    tags = sorted(Tag.objects.all(), key=lambda tag: -tag.num_members())
    l = '<div class="tagslist">' +\
        '\n'.join('<a href="{url}" class="listtag"><span class="tagtitle">{title}</span> <span class="tagsize">{size}</span></a>'.format(url=reverse("entry", args=["tag/" + tag.name]), title=tag.nice_title(), size=tag.num_members()) for tag in tags) +\
        '</div>'
    return value.replace("{{tagslist}}", l)

register.filter("tagslist", tagslist)

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
