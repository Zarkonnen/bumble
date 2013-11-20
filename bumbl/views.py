from django.shortcuts import render_to_response, get_object_or_404, redirect
from bumble.bumbl.models import Entry, Tag, Redirect
from django.utils.feedgenerator import Atom1Feed
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from bumble.bumbl.settings import PAGINATION, RECAPTCHA_PUBLIC, RECAPTCHA_PRIVATE
import json
from django.conf import settings
from django.utils.html import escape
from bumble.bumbl.templatetags.tags import filepaths, md, ensure_trailing_slash, urlify_path
from bumble.bumbl.forms import CommentForm
from django.core.context_processors import csrf
import requests
from django.utils import formats
from django.core.mail import send_mail, mail_admins
from datetime import datetime

def normalize_path(path):
    if path.endswith('/'):
        path = path[:-1]
    if path != '' and path[0] != '/':
        path = '/' + path
    return path

def tag_filter(tags, objects):
    if len(tags) == 0:
        return objects
    return tag_filter(tags[1:], objects.filter(tags__name__exact=tags[0]))

def get_tag_entries(tags, path):
    return tag_filter(tags, Entry.objects.filter(path__startswith=path+'/')).filter(created__lte=datetime.now()).order_by("-created")

def get_entry(path, request):
    entry = get_object_or_404(Entry, path=path)
    if entry.created > datetime.now() and not ("preview" in request.GET and request.GET["preview"] == entry.magic_number):
        raise Http404
    return entry

def entry(request, path):
    def entry_url(p):
        return request.build_absolute_uri(ensure_trailing_slash(reverse("bumble.bumbl.views.entry", args=[urlify_path(p)])))
    try:
        full_path = normalize_path(request.get_full_path())
        redirection = Redirect.objects.get(redirect_from=full_path)
        return redirect(link=entry_url(redirection.redirect_to), permanent=redirection.permanent)
    except:
        pass
    path = normalize_path(path)
    if path.endswith("/feed"):
        path = path[0:-len("/feed")]
        if "/tag/" in path:
            path, tags = path.split("/tag/")
            entry = get_entry(path, request)
            feed = Atom1Feed(title=entry.title + ":" + tags, description=tags, link=entry_url(path) + "tag/" + tags)
            entries = get_tag_entries(tags.split("+"), path)
            for e in entries:
                feed.add_item(title=e.title, description=md(filepaths(e.lead)), link=entry_url(e.path), pubdate=e.created)
            return HttpResponse(feed.writeString("UTF-8"), content_type="application/atom+xml")
        entry = get_entry(path, request)
        feed = Atom1Feed(title=entry.title, description=entry.lead, link=entry_url(path))
        entries = Entry.objects.filter(path__startswith=path+'/', created__lte=datetime.now()).order_by("-created")
        for e in entries:
            feed.add_item(title=e.title, description=md(filepaths(e.lead)), link=entry_url(e.path), pubdate=e.created)
        return HttpResponse(feed.writeString("UTF-8"), content_type="application/atom+xml")
    if "/tag/" in path:
        entry_path, tags = path.split("/tag/")
        return render_to_response('tag.html', {
            'media':settings.MEDIA_URL,
            'entry':get_entry(entry_path, request),
            'tags':tags.split("+"),
            "entries":get_tag_entries(tags.split("+"), entry_path)[0:PAGINATION],
            'pagination_url':reverse("bumble.bumbl.views.page", args=[578329023, urlify_path(path)]),
            'feed_url':entry_url(path) + "feed"
        })
    e = get_entry(path, request)
    recaptcha_error = None
    if request.method == "POST":
        form = CommentForm(request.POST)
        try:
            recaptcha_result = verify_recaptcha(request.META['REMOTE_ADDR'], request.POST['recaptcha_challenge_field'], request.POST['recaptcha_response_field'])
        except:
            return HttpResponseForbidden()
        if not recaptcha_result[0]:
            recaptcha_error = recaptcha_result[1]
        else:
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.entry = e
                new_comment.ip = request.META['REMOTE_ADDR']
                new_comment.save()
                mail_admins("New comment by " + new_comment.commenter, new_comment.text, html_message="<html><body><a href=\"" + entry_url(path) + "#" + str(new_comment.id) + "\">" + new_comment.commenter + "</a><br>" + new_comment.text + "</body></html>")
                return HttpResponseRedirect(request.path)
    else:
        form = CommentForm()
    c = {
        'media':settings.MEDIA_URL,
        'entry':e,
        'commentForm': form,
        'recaptcha_key': RECAPTCHA_PUBLIC,
        'recaptcha_error': recaptcha_error,
        'descendents':Entry.objects.filter(path__startswith=path+'/', created__lte=datetime.now()).order_by("-created")[0:PAGINATION],
        'pagination_url':reverse("bumble.bumbl.views.page", args=[578329023, urlify_path(path)]),
        'feed_url':entry_url(path) + "feed"
    }
    c.update(csrf(request))
    return render_to_response('entry.html', c)

def page(request, from_index, path):
    def entry_url(p):
        return request.build_absolute_uri(ensure_trailing_slash(reverse("bumble.bumbl.views.entry", args=[urlify_path(p)])))
    entries = []
    path = normalize_path(path)
    if "/tag/" in path:
        entry_path, tags = path.split("/tag/")
        entries = get_tag_entries(tags.split("+"), entry_path)
    else:
        entries = Entry.objects.filter(path__startswith=path+'/', created__lte=datetime.now()).order_by("-created")
    entries = entries[int(from_index)*PAGINATION:int(from_index)*PAGINATION + PAGINATION]
    return HttpResponse(json.dumps([{"title": escape(e.title), "created": formats.date_format(e.created, "DATETIME_FORMAT"), "description": md(filepaths(e.lead)), "link": entry_url(e.path)} for e in entries]))

def verify_recaptcha(ip, challenge, response):
    r = requests.post("http://www.google.com/recaptcha/api/verify", {'privatekey': RECAPTCHA_PRIVATE, 'remoteip': ip, 'challenge': challenge, 'response': response})
    if r.text.startswith("true"):
        return (True, None)
    else:
        return (False, r.text.splitlines()[1])
