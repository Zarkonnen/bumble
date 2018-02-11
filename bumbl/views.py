from django.shortcuts import render, get_object_or_404, redirect
from .models import Entry, Tag, Redirect, RawEntry
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404
from .settings import PAGINATION, RECAPTCHA_PUBLIC, RECAPTCHA_PRIVATE
import json, re, requests
from django.conf import settings
from django.utils.html import escape
from .templatetags.tags import filepaths, md, ensure_trailing_slash, urlify_path
from .forms import CommentForm
from django.utils import formats
from django.core.mail import send_mail, mail_admins
from django.utils.timezone import now
from django.utils.encoding import force_text
from .feed import BumbleFeed

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
    return tag_filter(tags, Entry.objects.filter(path__startswith=path+'/')).filter(created__lte=now()).order_by("-created")

def get_entry(path, request):
    entry = get_object_or_404(Entry, path=path)
    if entry.created > now() and not ("preview" in request.GET and request.GET["preview"] == entry.magic_number):
        raise Http404
    return entry

def entry(request, path):
    def entry_url(p):
        return request.build_absolute_uri(ensure_trailing_slash(reverse("entry", args=[urlify_path(p)])))
    try:
        full_path = normalize_path(request.get_full_path())
        redirection = Redirect.objects.get(redirect_from=full_path)
        return redirect(link=entry_url(redirection.redirect_to), permanent=redirection.permanent)
    except:
        pass
    def add_feed_entry(feed, e):
        feed.add_item(
            title=e.title,
            description=md(filepaths(e.lead)),
            link=entry_url(e.path),
            pubdate=e.created,
            updateddate=e.created,
            content=force_text(md(filepaths(e.all_content)), strings_only=True),
            base_content=force_text(md(filepaths(e.content)), strings_only=True),
            author_name=settings.FEED_AUTHOR_NAME,
            author_email=settings.FEED_AUTHOR_EMAIL,
            author_link=settings.FEED_AUTHOR_LINK,
            categories=[t.nice_title() for t in e.tags.all()]
            )
    
    path = normalize_path(path)
    try:
        raw_entry = RawEntry.objects.get(path=path[1:])
        return HttpResponse(raw_entry.content, content_type=raw_entry.content_type)
    except RawEntry.DoesNotExist:
        pass
    if path.endswith("/feed"):
        path = path[0:-len("/feed")]
        if "/tag/" in path:
            path, tags = path.split("/tag/")
            entry = get_entry(path, request)
            feed = BumbleFeed(
                title=entry.title + ":" + tags,
                description=tags,
                link=entry_url(path) + "tag/" + tags,
                feed_url=entry_url(path) + "tag/" + tags + "/feed"
                )
            entries = get_tag_entries(tags.split("+"), path)
            for e in entries:
                add_feed_entry(feed, e)
            return HttpResponse(feed.writeString("UTF-8"), content_type="application/atom+xml")
        entry = get_entry(path, request)
        feed = BumbleFeed(
            title=entry.title,
            description=entry.lead,
            link=entry_url(path),
            feed_url=entry_url(path) + "/feed"
            )
        entries = Entry.objects.filter(path__startswith=path+'/', created__lte=now()).order_by("-created")
        for e in entries:
            add_feed_entry(feed, e)
        return HttpResponse(feed.writeString("UTF-8"), content_type="application/atom+xml")
    if "/tag/" in path:
        entry_path, tags = path.split("/tag/")
        tag_names = tags.split("+")
        tag = None
        if len(tag_names) == 1:
            tag = get_object_or_404(Tag, name=tag_names[0])
        return render(request, 'tag.html', {
            'media':settings.MEDIA_URL,
            'entry':get_entry(entry_path, request),
            'tags':tag_names,
            'tag': tag,
            "entries":get_tag_entries(tag_names, entry_path)[0:PAGINATION],
            'pagination_url':reverse("page", args=[578329023, urlify_path(path)]),
            'feed_url':entry_url(path) + "feed"
        })
    e = get_entry(path, request)
    recaptcha_error = None
    if request.method == "POST":
        form = CommentForm(request.POST)
        try:
            recaptcha_result = verify_recaptcha(request.META['REMOTE_ADDR'], request.POST['g-recaptcha-response'])
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
        'media': settings.MEDIA_URL,
        'entry': e,
        'commentForm': form,
        'recaptcha_key': RECAPTCHA_PUBLIC,
        'recaptcha_error': recaptcha_error,
        'descendents': Entry.objects.filter(path__startswith=path+'/', created__lte=now()).order_by("-created")[0:PAGINATION],
        'pagination_url': reverse("page", args=[578329023, urlify_path(path)]),
        'feed_url': entry_url(path) + "feed",
        'user': request.user
    }
    return render(request, 'entry.html', c)

def page(request, from_index, path):
    def entry_url(p):
        return request.build_absolute_uri(ensure_trailing_slash(reverse("entry", args=[urlify_path(p)])))
    entries = []
    path = normalize_path(path)
    if "/tag/" in path:
        entry_path, tags = path.split("/tag/")
        entries = get_tag_entries(tags.split("+"), entry_path)
    else:
        entries = Entry.objects.filter(path__startswith=path+'/', created__lte=now()).order_by("-created")
    entries = entries[int(from_index)*PAGINATION:int(from_index)*PAGINATION + PAGINATION]
    return HttpResponse(json.dumps([{"title": escape(e.title), "created": formats.date_format(e.created, "DATETIME_FORMAT"), "description": md(filepaths(e.lead)), "link": entry_url(e.path)} for e in entries]))

def verify_recaptcha(ip, response):
    r = requests.post("https://www.google.com/recaptcha/api/siteverify", {'secret': RECAPTCHA_PRIVATE, 'remoteip': ip, 'response': response})
    if r.json()["success"]:
        return (True, None)
    else:
        return (False, "You may be a robot, sorry.")
