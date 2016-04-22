from django.contrib import admin
from django.utils.html import strip_tags
from django.template.defaultfilters import safe

from models import MailOutTemplate


def go_to_template(self):
    return '<div style="text-align:center; font-weight: bold; padding: 2px 5px; background: #ccc;"><a href="view-source:http://tbr.webfactional.com/mailout/%s/" target="_blank">TEMPLATE</a></div>' % self.id
go_to_template.allow_tags = True


def intro_text(self):
    try:
        text = strip_tags(self.intro)
        if text[65]:
            return '%s ...' % text[:64]
        else:
            return text
    except:
        pass
intro_text.allow_tags = True


class MailOutAdmin(admin.ModelAdmin):
    list_display = ['subject', intro_text, 'date', go_to_template]
    filter_horizontal = ['upcoming_events']


admin.site.register(MailOutTemplate, MailOutAdmin)
