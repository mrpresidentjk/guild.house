import datetime
from django.contrib import admin
from models import Event, EventDate, EventUser, EventGallery
from forms import EventAdminForm


class EventUserInline(admin.TabularInline):
    model = EventUser
    extra = 1

class EventDateInline(admin.TabularInline):
    model = EventDate
    extra = 1

    def queryset(self, request):
        try:
            qs = super(EventDateInline, self).queryset(request)
            if qs.count()>10:
                limit = datetime.datetime.today()-datetime.timedelta(weeks=8)
                qa = qs.filter(date__gte=limit)
                if qa.count()<8:
                    limit = datetime.datetime.today()-datetime.timedelta(weeks=35)
                    return qs.filter(date__gte=limit)
                else:
                    return qa

        except: pass


def event_thumb(self):
    return u'<img src="%s">' % self.main_image.get_admin_thumbnail_url()
event_thumb.short_description = "Main image"
event_thumb.allow_tags = True

def event_poster(self):
    return u'<img src="%s">' % self.poster.get_admin_poster_thumb_url()
event_poster.short_description = "Poster image"
event_poster.allow_tags = True

def recur(self):
    if self.recurring:
        return '<img src="/admin_media/img/admin/icon-yes.gif" alt="True">'
    else:
        return ''
recur.short_description = "Recur"
recur.allow_tags = True

class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm

    list_filter = ['spotlight', 'recurring']
    list_display = [recur, 'event_name', 'date', 'time', 'spotlight', 'slug']#, event_thumb, event_poster]
    list_display_links = ('event_name',)
    inlines = [EventUserInline, EventDateInline]
    filter_horizontal = ['extra_images']
    fieldsets = (
        (None, {
            'fields': ('event_name', 'date', 'time', 'paypal', 'door_cost', 'ticket_url', 'gig_details')
        }),
        ('Extra Details', {
            'classes': ('collapse',),
            'fields': ('content', 'spotlight', 'poster', 'main_image', 'extra_URLs', 'post_event_gallery', 'extra_images', 'twitter_account', 'facebook_event')
        }),
        ('Recurring Event Details', {
            'classes': ('collapse',),
            'fields': ('recurring', 'recur_description')
        }),
    )


def date_thumb(self):
    return u'<img src="%s" height="20" width="20">' % self.main_image.get_admin_thumbnail_url()
date_thumb.short_description = "Img"
date_thumb.allow_tags = True

class EventDateAdmin(admin.ModelAdmin):
    list_display = ['event', 'date', 'time', 'date_image', date_thumb]


admin.site.register(Event, EventAdmin)
admin.site.register(EventDate, EventDateAdmin)
