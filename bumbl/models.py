from django.db import models

class Entry(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        abstract = True
        
class Page(Entry):
    title = models.CharField(max_length=1000)
    content = models.TextField()
    def __unicode__(self):
        return self.title
    
class Update(Entry):
    title = models.CharField(max_length=1000)
    page = models.ForeignKey(Page)
    def __unicode__(self):
        return self.title

class Link(Entry):
    url = models.URLField('URL', max_length=1000)
    def __unicode__(self):
        return self.url
    
class PictureEntry(Entry):
    name = models.CharField(max_length=1000)
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name_plural = "picture entries"
    
