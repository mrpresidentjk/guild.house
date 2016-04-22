from django.contrib import admin

from models import FoodBevPromo


def food_thumb(self):
    if self.poster:
        return u'<img src="%s">' % self.poster.get_admin_thumbnail_url()
    if self.banner:
        return u'<img src="%s">' % self.banner.get_admin_thumbnail_url()
food_thumb.short_description = "Graphic"
food_thumb.allow_tags = True
    

class FoodBevAdmin(admin.ModelAdmin):
    list_display = [food_thumb, 'name', 'active', 'order']
    list_display_links = [food_thumb, 'name']
    list_editable = ['order']


admin.site.register(FoodBevPromo, FoodBevAdmin)
