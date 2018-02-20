import datetime
from . import querysets
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible
from photologue.models import Photo, Gallery
from taggit.managers import TaggableManager

from project.utils import get_current_site

def photo_default_main(self=None):
    if self:
        return self.main_image

def photo_default_poster(self=None):
    if self:
        return self.poster


@python_2_unicode_compatible
class Event(models.Model):
    is_enabled  = models.BooleanField(default=True)

    spotlight   = models.BooleanField(default=False)
    spotlight_order = models.IntegerField(default=0)
    recurring   = models.BooleanField(default=False)
    recur_description  = models.CharField(max_length=255, verbose_name="Date Description",
                                          help_text="eg, 'Every Thursday'", blank=True, default='')
    event_image = models.ForeignKey(
        Photo,
        blank=True, null=True,
        related_name="event_image",
    )
    main_image  = models.ForeignKey(
        Photo,
        blank=True, null=True,
        related_name="main_image",
    )
    poster      = models.ForeignKey(
        Photo,
        blank=True, null=True,
        related_name="poster",
    )

    event_name  = models.CharField(max_length=255)
    slug        = models.SlugField(max_length=255, blank=True, default='')
    date        = models.DateField(blank=True, null=True, help_text="Events without dates aren't displayed, except if recurring.")
    time        = models.TimeField(blank=True, null=True,
                                   help_text="24 HOUR TIME. Add a usual time for recurring events. This will be over-ridden if specific time added.")

    expires = models.DateField(blank=True, null=True, help_text="Optional.")

    paypal = models.CharField(max_length=65, blank=True, default='',
                              help_text="Paypal provided hosted_button_id")
    door_cost   = models.CharField(max_length=255, blank=True, default='', verbose_name='cost')
    ticket_url  = models.URLField(blank=True, default='',
        help_text="External ticket URL (if applicable)")
    gig_details = models.TextField(max_length=999, verbose_name="Snippet Text",
        help_text="Short text. LIMITED TO 175 words.")
    content = models.TextField(blank=True, default='',
        help_text="More artist info / bio.")
    extra_URLs  = models.TextField(blank=True, default='',
        help_text="eg. artist Myspace / website, separate multiple urls  with commas.")
    post_event_gallery = models.ForeignKey(Gallery, blank=True, null=True)

    extra_images = models.ManyToManyField(
        Photo, blank=True,
    )

    twitter_account = models.CharField(max_length=100, blank=True, default='')
    facebook_event = models.CharField(max_length=255, blank=True, default='')

    tags = TaggableManager(blank=True)

    objects = querysets.QuerySet.as_manager()

    def save(self):
        self.slug = slugify(self.event_name)
        if self.spotlight and not self.spotlight_order:
            self.spotlight_order = '999'

        ## set event_image (hidden field with absolute version)
        if not self.event_image:
            if self.main_image:
                self.event_image = self.main_image
            elif self.poster:
                self.event_image = self.poster
            else:
                pass

        super(Event, self).save()
        ## handle date object: ~ add if not || ~ correct image
        e = EventDate.objects.filter(event=self) #, date=self.date)
        if e:
            today = datetime.datetime.today()
            d = e.filter(date__gte=today)
            if d:
                c = d.order_by('date')[0]
                self.date = c.date
                if c.date_image:
                    self.event_image = c.date_image
        else:
            e = EventDate(event=self, date=self.date)
            e.save()
        super(Event, self).save()

    def __str__(self):
        return self.event_name


    class Meta:
        ordering = ['-date', '-recurring']


class EventDate(models.Model):
    event = models.ForeignKey(Event)
    date  = models.DateField()
    time  = models.TimeField(blank=True, null=True)
    additional = models.CharField(max_length=999, blank=True,
                                  default='', help_text="Make it special.")
    date_image  = models.ForeignKey(
        Photo,
        blank=True, null=True,
        related_name="date_image",
        )

    def __unicode__(self):
        return '%s -- %s' % (self.date, self.event.event_name)


    class Meta:
        ordering = ['-date']


class EventGallery(models.Model):
    event = models.ForeignKey(Event)
    photo = models.ForeignKey(Photo)
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return self.event.event_name


class EventVideo(models.Model):
    event = models.ForeignKey(Event)
    video = models.CharField(max_length=255,
                             verbose_name="Youtube video",
                             help_text="YouTube video link.")
    order = models.IntegerField(default=0)

    ## s.find('v=').split('&')[0]
    ## http://www.youtube.com/watch?v=3I6jWE5UIYg&feature=related

    def save(self):
        if not self.order:
            self.order = '999'
        v = self.video
        if v[:4] == 'http':
            self.video = v[v.find('v=')+2:].split('&')[0]
            #"http://www.youtube.com/v/%s&hl=en&fs=1" % v
        super(EventVideo, self).save()

    def __unicode__(self):
        return '%s -- %s' % (self.event.event_name, self.video)

    class Meta:
        ordering = ['order']


class EventUser(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, blank=True, default='')
    number_tickets = models.IntegerField(null=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def save(self):
        if not self.order:
            self.order = '999'
        super(ComingEvent, self).save()

    class Meta:
        ordering = ['event']
