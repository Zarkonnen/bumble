from django.db import models
from django.core.exceptions import ValidationError
import datetime
from django.utils.timezone import now
from hashlib import sha256
from django.conf import settings

class File(models.Model):
    name = models.CharField(max_length=1000)
    f = models.FileField(upload_to="uploads")
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=1000)
    title = models.CharField(max_length=1000, default="")
    content = models.TextField(blank=True, default="", help_text="""Use *** to denote text for markdown.<br>Use {{f:filename}} to get the path of a file.""")
    css = models.TextField(blank=True, default="")
    def nice_title(self):
        if self.title:
            return self.title
        return self.name
    def num_members(self):
        return len(self.entries.all())
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["name"]

class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    commenter = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    ip = models.CharField(max_length=100)
    text = models.CharField(max_length=5000)
    entry = models.ForeignKey("Entry")
    def __str__(self):
        return self.commenter + ": " + self.text[:100]

class Entry(models.Model):
    created = models.DateTimeField(default=datetime.datetime.now)
    title = models.CharField(max_length=1000)
    slug = models.SlugField(blank=True)
    css = models.TextField(blank=True)
    local_css = models.TextField(blank=True)
    total_css = models.TextField(blank=True)
    lead = models.TextField(blank=True)
    content = models.TextField(blank=True, help_text="""Use *** to denote text for markdown.<br>Use {{f:filename}} to get the path of a file.""")
    section_content = models.TextField(blank=True, help_text="""Included in all descendents. Use *** to denote text for markdown.<br>Use {{f:filename}} to get the path of a file.""")
    total_section_content = models.TextField(blank=True)
    parent = models.ForeignKey("self", blank=True, null=True, related_name="children")
    path = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="entries")
    commentsOn = models.BooleanField(default=True, help_text="""Check to allow new comments on a page. Existing comments will be displayed even when this is unchecked.""")
    def clean(self):
        e = self.parent
        while e:
            if e == self:
                raise ValidationError('An entry cannot be its own ancestor.')
            e = e.parent
    def save(self, *args, **kwargs):
        self.path = self.calculate_path()
        self.total_css = self.calculate_total_css()
        self.total_section_content = self.calculate_total_section_content()
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
    def calculate_total_css(self):
        l = [self.css]
        e = self.parent
        while e:
            l.append(e.css)
            e = e.parent
        return "\n\n".join(l[::-1]) + "\n\n" + self.local_css
    def calculate_total_section_content(self):
        l = [self.section_content]
        e = self.parent
        while e:
            l.append(e.section_content)
            e = e.parent
        return "\n\n".join(l[::-1])
    @property
    def all_content(self):
        return self.lead + self.calculate_total_section_content() + self.content
    def sorted_comments(self):
        return self.comment_set.order_by('created')
    @property
    def url_path(self):
        if self.path == "":
            return ""
        return self.path[1:]
    @property
    def magic_number(self):
        return sha256((self.path + settings.SECRET_KEY).encode('utf-8')).hexdigest()
    @property
    def preview_postfix(self):
        if self.created > now():
            return "?preview=" + self.magic_number
        else:
            return ""
    def __str__(self):
        if self.created > now():
            return "SCHEDULED: " + str(self.created) + ": " + self.title
        return self.title
    class Meta:
        verbose_name_plural = "entries"
        ordering = ["-created"]

class Redirect(models.Model):
    redirect_from = models.CharField(max_length=1000, help_text="""Path format: starting slash, no trailing slash. Example: "/foo".""")
    redirect_to = models.CharField(max_length=1000, help_text="""Path format: starting slash, no trailing slash. Example: "/foo".""")
    permanent = models.BooleanField(default=True)
    def __str__(self):
        if self.permanent:
            return self.redirect_from + " => " + self.redirect_to
        return self.redirect_from + " -> " + self.redirect_to

class RawEntry(models.Model):
    path=models.CharField(max_length=1000)
    content=models.TextField(blank=True)
    content_type=models.CharField(max_length=1000, default="text/html")
    def __str__(self):
        return self.path
    class Meta:
        verbose_name_plural="raw entries"
        ordering=["path"]
