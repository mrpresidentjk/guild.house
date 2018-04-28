# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from project import utils
from taggit.managers import TaggableManager

from . import querysets


def get_current_site():
    try:
        return Site.objects.get_current().pk
    except Site.DoesNotExist:
        pass


@python_2_unicode_compatible
class Category(models.Model):

    name = models.CharField(max_length=200)

    title = models.CharField(max_length=200, blank=True, default='')

    heading = models.CharField(max_length=200, blank=True, default='')

    featured_content = models.TextField(blank=True, default='')

    content = models.TextField(blank=True, default='')

    meta_description = models.CharField(max_length=200, blank=True, default='')

    is_enabled = models.BooleanField('enabled', db_index=True, default=True)

    is_featured = models.BooleanField('featured', db_index=True, default=False)

    site = models.ForeignKey('sites.Site', default=get_current_site,
                             related_name='library_categories',
                             on_delete=models.PROTECT)

    slug = models.SlugField()

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    updated_at = models.DateTimeField(auto_now=True, editable=False)

    objects = querysets.QuerySet.as_manager()

    class Meta(object):
        ordering = ['name']
        unique_together = ['site', 'slug']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('library:category_detail', kwargs={'slug': self.slug})

    def is_active(self):
        return self in self.__class__.objects.filter(pk=self.pk).active()
    is_active.boolean = True
    is_active.short_description = 'active'

    def save(self, *args, **kwargs):
        if not self.slug:
            queryset = self.__class__.objects.filter(site=self.site)
            self.slug = utils.generate_unique_slug(self.name, queryset)
        return super(Category, self).save(*args, **kwargs)


@python_2_unicode_compatible
class Game(models.Model):

    name = models.CharField(max_length=200)

    categories = models.ManyToManyField(
        'library.Category', related_name='games', related_query_name='game')

    expansion_for = models.ForeignKey(
        'self', related_name='expansions', related_query_name='expansion',
        blank=True, null=True, on_delete=models.PROTECT)

    publisher = models.CharField(max_length=200, blank=True, default='')

    boardgamegeek_id = models.PositiveIntegerField(blank=True, null=True)

    boardgamegeek_rank = models.PositiveIntegerField(blank=True, null=True)

    minimum_players = models.PositiveIntegerField(blank=True, null=True)

    maximum_players = models.PositiveIntegerField(blank=True, null=True)

    minimum_playtime = models.PositiveIntegerField(
        blank=True, null=True, help_text='Duration in minutes')

    maximum_playtime = models.PositiveIntegerField(
        blank=True, null=True, help_text='Duration in minutes')

    year_published = models.PositiveIntegerField(blank=True, null=True)

    title = models.CharField(max_length=200, blank=True, default='')

    heading = models.CharField(max_length=200, blank=True, default='')

    featured_content = models.TextField(blank=True, default='')

    content = models.TextField(blank=True, default='')

    tags = TaggableManager(blank=True)

    meta_description = models.CharField(max_length=200, blank=True, default='')

    is_enabled = models.BooleanField('enabled', db_index=True, default=True)

    is_featured = models.BooleanField('featured', db_index=True, default=False)

    site = models.ForeignKey('sites.Site', default=get_current_site,
                             related_name='library_games',
                             on_delete=models.PROTECT)

    slug = models.SlugField()

    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    updated_at = models.DateTimeField(auto_now=True, editable=False)

    objects = querysets.QuerySet.as_manager()

    class Meta(object):
        ordering = ['name']
        unique_together = ['site', 'slug']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('library:game_detail', kwargs={'slug': self.slug})

    def is_active(self):
        return self in self.__class__.objects.filter(pk=self.pk).active()
    is_active.boolean = True
    is_active.short_description = 'active'

    def is_expansion(self):
        return bool(self.expansion_for)
    is_expansion.boolean = True
    is_expansion.short_description = 'expansion'

    def save(self, *args, **kwargs):
        if not self.slug:
            queryset = self.__class__.objects.filter(site=self.site)
            self.slug = utils.generate_unique_slug(self.name, queryset)
        return super(Game, self).save(*args, **kwargs)
