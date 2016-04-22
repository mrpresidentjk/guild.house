from django.db import models
from photologue.models import Photo


class FoodBevPromo(models.Model):
    active = models.BooleanField(default=True)
    poster = models.ForeignKey(Photo, null=True, blank=True, related_name="food_poster")
    banner = models.ForeignKey(Photo, null=True, blank=True, related_name="food_banner")
    name = models.CharField(max_length=150)
    text = models.TextField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self):
        if not self.order:
            self.order = '999'       
        super(FoodBevPromo, self).save()


    class Meta:
        ordering = ['active', '-id']
        verbose_name = 'Food/Beverage Promo'

    
    
