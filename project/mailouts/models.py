import datetime

from django.db import models

from events.models import Event
from food_beverages.models import FoodBevPromo

today = datetime.datetime.today()
EVENT_SPOTLIGHT = {'spotlight': True}#, 'date__gte': today}
#EVENT_UPCOMING = {'spotlight': False}#, 'date__gte': today}
FB_ACTIVE = {'active': True}


class MailOutTemplate(models.Model):
    date = models.DateField(auto_now_add=True)    
    subject = models.CharField(max_length=50, help_text="E-mail subject")
    intro = models.TextField(null=True, blank=True)
    spotlight = models.ForeignKey(Event, limit_choices_to=EVENT_SPOTLIGHT, null=True, blank=True,
                                  related_name="mailout_spotlight")
    upcoming_events =  models.ManyToManyField(Event, null=True, blank=True, #limit_choices_to=EVENT_UPCOMING, 
                                              related_name="mailout_event")
    food_bev  = models.ForeignKey(FoodBevPromo, limit_choices_to=FB_ACTIVE, null=True, blank=True,
                                  verbose_name="Food & Beverage Promo",
                                  help_text="Must have 'banner' image to show.")

    def __unicode__(self):
        return self.subject

    class Meta:
        ordering = ['-id']


