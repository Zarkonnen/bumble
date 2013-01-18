from django.db import models

class File(models.Model):
    name = models.CharField(max_length=1000)
    f = models.FileField(upload_to="uploads")
    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=1000)
    def __unicode__(self):
        return self.name

class Entry(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=1000)
    slug = models.SlugField(blank=True)
    css = models.TextField(blank=True)
    lead = models.TextField(blank=True)
    content = models.TextField(blank=True)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="children")
    path = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="entries")
    def save(self, *args, **kwargs):
        self.path = self.calculate_path()
        super(Entry, self).save(*args, **kwargs)
        for c in self.children.all():
            c.save()
    def calculate_path(self):
        l = [self.slug]
        e = self.parent
        while e:
            l.append(e.slug)
            e = e.parent
        return "/".join(l[::-1])
	@property
	def url_path(self):
		if self.path == "":
			return ""
		return self.path[1:]
    def __unicode__(self):
        return self.title
    class Meta:
        verbose_name_plural = "entries"

