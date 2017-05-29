# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from debug_toolbar import urls as debug_toolbar_urls
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from project.sitemaps import sitemaps


urlpatterns = [

    # Site
    url(r'^', include('project.site.urls')),

    # Blog
    url(r'^blog/', include('project.blog.urls')),

    # Menu
    url(r'^menus/', include('project.menus.urls')),

##     # Events
##     url(r'^events/', include('project.events.urls')),

    # Library
    url(r'^library/', include('project.library.urls')),

    # Robots
    url(r'^robots\.txt$', include('robots.urls')),

    # XML Sitemap
    url(r'^sitemap.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),

    ## Admin Docs
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Admin
    url(r'^admin/', include(admin.site.urls)),

    # TinyMCE
    url(r'^tinymce/', include('tinymce.urls')),

]


if settings.DEBUG:
    # Only serve media files if in a development environment
    from django.conf.urls.static import static
    from django.views.generic import TemplateView

    urlpatterns += [
        url(r'^errors/404$', TemplateView.as_view(template_name='404.html')),
        url(r'^errors/500$', TemplateView.as_view(template_name='500.html')),
        url(r'^__debug__/', include(debug_toolbar_urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
