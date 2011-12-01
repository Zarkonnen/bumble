from django.shortcuts import render_to_response
from bumble.bumbl.models import Entry

def entry(request, path):
    if path.endswith('/'):
        path = path[:-1]
    if path != '':
        path = '/' + path
    return render_to_response('base.html', {'entry':Entry.objects.get(path=path), 'descendents':Entry.objects.filter(path__startswith=path+'/')})
