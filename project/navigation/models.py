from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name
    

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu)
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=999)
    order = models.IntegerField()

    def __unicode__(self):
        return self.name
    
