import datetime
from django.db import models
from photologue.models import Photo, Gallery
from django.template.defaultfilters import slugify


## return Photo.object.filter(galleries=None, eventgallery=None, main_image=None, poster=None)

def photo_default_main(self=None):
    if self:
        return self.main_image

def photo_default_poster(self=None):
    if self:
        return self.poster

try:
    DEFAULT_IMAGE = Photo.objects.get(pk=56)
except: pass
PHOTO_MAIN = {'galleries': None, 'event':None}#, 'main_image': None}#, 'eventgallery': None, 'poster': None}
PHOTO_POSTER = {}#{'galleries': None, 'eventgallery': None, 'main_image': None}
PHOTO_EXTRA = {}#{'galleries': None, 'eventgallery': None, 'poster': None, 'main_image': None}
GALLERY = {'galleries': None, 'eventgallery': None, 'poster': None, 'main_image': None}

class Event(models.Model):
    spotlight   = models.BooleanField(default=False)
    spotlight_order = models.IntegerField(default=0)
    recurring   = models.BooleanField(default=False)
    recur_description  = models.CharField(max_length=255, verbose_name="Date Description",
                                          help_text="eg, 'Every Thursday'", blank=True, null=True)
    event_image = models.ForeignKey(
        Photo,
        blank=True, null=True,
        related_name="event_image",
        ## default=photo_default_main,
        )
    main_image  = models.ForeignKey(
        Photo,
        blank=True, null=True,
        related_name="main_image",
        ## limit_choices_to = PHOTO_MAIN,
        ## verbose_name="Square Event Image",
        ## default=photo_default_main,
        )
    poster      = models.ForeignKey(
        Photo,
        blank=True, null=True,
        related_name="poster",
        ## default=photo_default_poster,
        ## limit_choices_to = PHOTO_POSTER,
        )

    event_name  = models.CharField(max_length=255)
    slug        = models.SlugField(max_length=255, blank=True, null=True)
    date        = models.DateField(blank=True, null=True, help_text="Events without dates aren't displayed, except if recurring.")
    time        = models.TimeField(blank=True, null=True,
                                   help_text="24 HOUR TIME. Add a usual time for recurring events. This will be over-ridden if specific time added.")
    door_cost   = models.CharField(max_length=255, blank=True, null=True, verbose_name='cost')
    ticket_url  = models.URLField(blank=True, null=True,
        help_text="External ticket URL (if applicable)")
    gig_details = models.TextField(max_length=999, verbose_name="Snippet Text",
        help_text="Short text. LIMITED TO 175 words.")
    extra_details = models.TextField(blank=True, null=True,
        help_text="More artist info / bio.")
    extra_URLs  = models.TextField(blank=True, null=True,
        help_text="eg. artist Myspace / website, separate multiple urls  with commas.")
    post_event_gallery = models.ForeignKey(Gallery, blank=True, null=True)

    extra_images = models.ManyToManyField(
        Photo, blank=True,
        ## related_name="extra_images",
        ## help_text="eg. album images, bio shots",
        ## limit_choices_to = PHOTO_EXTRA,
        )

    twitter_account = models.CharField(max_length=100, blank=True, null=True)
    facebook_event = models.CharField(max_length=255, blank=True, null=True)


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
                #self.event_image = DEFAULT_IMAGE

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

    def __unicode__(self):
        return self.event_name


    class Meta:
        ordering = ['-date', '-recurring']


class EventDate(models.Model):
    event = models.ForeignKey(Event)
    date  = models.DateField()
    time  = models.TimeField(blank=True, null=True)
    additional = models.CharField(max_length=999, blank=True, null=True, help_text="Make it special.")
    date_image  = models.ForeignKey(
        Photo,
        blank=True, null=True,
        related_name="date_image",
        ## verbose_name="Square Event Image",
        ## limit_choices_to = PHOTO_MAIN,
        )

    ## def save(self):
    ##     super(EventDate, self).save()
    ##     #self.event.save()

    def __unicode__(self):
        return '%s -- %s' % (self.date, self.event.event_name)


    class Meta:
        ordering = ['-date']


class ComingEvent(models.Model):
    active = models.BooleanField(default=True)
    coming_event = models.CharField(max_length=255)
    url = models.URLField(blank=True, null=True)
    expires = models.DateField(blank=True, null=True, help_text="Optional.")
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return self.coming_event

    def save(self):
        if not self.order:
            self.order = '999'
        super(ComingEvent, self).save()


    class Meta:
        ordering = ['active', 'order']


class EventGallery(models.Model):
    event = models.ForeignKey(Event)
    photo = models.ForeignKey(Photo)
    order = models.IntegerField(default=0)

    def __unicode__(self):
        return self.event.event_name


class EventVideo(models.Model):
    event = models.ForeignKey(Event)
    video = models.CharField(max_length=255, verbose_name="Youtube video", help_text="YouTube video link.")
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
