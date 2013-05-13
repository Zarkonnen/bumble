from django.shortcuts import render_to_response, get_object_or_404
from bumble.bumbl.models import Entry, Tag
from django.utils.feedgenerator import Atom1Feed
from django.core.urlresolvers import reverse
from bumble.bumbl.templatetags.tags import urlify_path
from django.http import HttpResponse, HttpResponseRedirect
from bumble.bumbl.settings import PAGINATION
import json
from django.conf import settings
from django.utils.html import escape
from bumble.bumbl.templatetags.tags import filepaths, md
from bumble.bumbl.forms import CommentForm
from django.core.context_processors import csrf

def tag_filter(tags, objects):
    if len(tags) == 0:
        return objects
    return tag_filter(tags[1:], objects.filter(tags__name__exact=tags[0]))

def get_tag_entries(tags, path):
    return tag_filter(tags, Entry.objects.filter(path__startswith=path+'/')).order_by("-created")

def entry(request, path):
    if path.endswith('/'):
        path = path[:-1]
    if path != '':
        path = '/' + path
    if path.endswith("/feed"):
        path = path[0:-len("/feed")]
        if "/tag/" in path:
            path, tags = path.split("/tag/")
            entry = get_object_or_404(Entry, path=path)
            feed = Atom1Feed(title=entry.title + ":" + tags, description=tags, link=reverse("bumble.bumbl.views.entry", args=[urlify_path(path)])+"/tag/"+tags)
            entries = get_tag_entries(tags.split("+"), path)
            for e in entries:
                feed.add_item(title=e.title, description=e.lead, link=reverse("bumble.bumbl.views.entry", args=[urlify_path(e.path)]))
            return HttpResponse(feed.writeString("UTF-8"))
        entry = get_object_or_404(Entry, path=path)
        feed = Atom1Feed(title=entry.title, description=entry.lead, link=reverse("bumble.bumbl.views.entry", args=[urlify_path(path)]))
        entries = Entry.objects.filter(path__startswith=path+'/').order_by("-created")
        for e in entries:
            feed.add_item(title=e.title, description=e.lead, link=reverse("bumble.bumbl.views.entry", args=[urlify_path(e.path)]))
        return HttpResponse(feed.writeString("UTF-8"))
    if "/tag/" in path:
        entry_path, tags = path.split("/tag/")
        return render_to_response('tag.html', {'media':settings.MEDIA_URL, 'entry':get_object_or_404(Entry, path=entry_path), 'tags':tags.split("+"), "entries":get_tag_entries(tags.split("+"), entry_path)[0:PAGINATION], 'pagination_url':reverse("bumble.bumbl.views.page", args=[578329023, urlify_path(path)])})
    e = get_object_or_404(Entry, path=path)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.entry = e
            new_comment.ip = request.META['REMOTE_ADDR']
            new_comment.save()
            return HttpResponseRedirect(request.path)
    else:
        form = CommentForm()
    c = {'media':settings.MEDIA_URL, 'entry':e, 'commentForm': form, 'descendents':Entry.objects.filter(path__startswith=path+'/').order_by("-created")[0:PAGINATION], 'pagination_url':reverse("bumble.bumbl.views.page", args=[578329023, urlify_path(path)])}
    c.update(csrf(request))
    return render_to_response('entry.html', c)

def page(request, from_index, path):
    entries = []
    if path.endswith('/'):
        path = path[:-1]
    if path != '':
        path = '/' + path
    if "/tag/" in path:
        entry_path, tags = path.split("/tag/")
        entries = get_tag_entries(tags.split("+"), entry_path)
    else:
        entries = Entry.objects.filter(path__startswith=path+'/').order_by("-created")
    entries = entries[int(from_index)*PAGINATION:int(from_index)*PAGINATION + PAGINATION]
    return HttpResponse(json.dumps([{"title": escape(e.title), "created": e.created, "description": md(filepaths(e.lead)), "link": reverse("bumble.bumbl.views.entry", args=[urlify_path(e.path)])} for e in entries]))

        
