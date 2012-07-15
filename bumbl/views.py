from django.shortcuts import render_to_response, get_object_or_404
from bumble.bumbl.models import Entry, Tag

def entry(request, path):
    if path.endswith('/'):
        path = path[:-1]
    if path != '':
        path = '/' + path
    if "/tag/" in path:
        path, tag = path.split("/tag/")
        return render_to_response('tag.html', {'tag':tag, "entries":Entry.objects.filter(tags__name__exact=tag, path__startswith=path+'/')})
    return render_to_response('base.html', {'entry':get_object_or_404(Entry, path=path), 'descendents':Entry.objects.filter(path__startswith=path+'/')})


