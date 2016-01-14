# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf import settings
from django.core.files.storage import get_storage_class
from storages.backends.s3boto import S3BotoStorage


class StaticS3BotoStorage(S3BotoStorage):

    def __init__(self, *args, **kwargs):
        defaults = {
            'bucket_name': 'static',
            'custom_domain': 'static.cloudfront.net',
            'default_acl': 'public-read',
            'file_overwrite': True,
            'headers': {'Cache-Control': b'public, max-age=604800'},
            'preload_metadata': True,
            'querystring_auth': False,
            'secure_urls': True,
            'url_protocol': 'https:'}
        for key, value in defaults.items():
            kwargs.setdefault(key, value)
        super(StaticS3BotoStorage, self).__init__(*args, **kwargs)

        if 'compressor' in settings.INSTALLED_APPS:
            self.local_storage = get_storage_class(
                'compressor.storage.CompressorFileStorage')()

    def save(self, name, content):
        non_gzipped_content_file = content.file
        name = super(StaticS3BotoStorage, self).save(name, content)
        if 'compressor' in settings.INSTALLED_APPS:
            content.file = non_gzipped_content_file
            self.local_storage._save(name, content)
        return name

    def url(self, name):
        # Fix for http://code.larlet.fr/django-storages/issue/121/s3boto-admin-prefix-issue-with-django-14  # NOQA
        url = super(StaticS3BotoStorage, self).url(name)
        if name.endswith('/') and not url.endswith('/'):
            url += '/'
        return url


class PublicMediaS3BotoStorage(S3BotoStorage):

    def __init__(self, *args, **kwargs):
        defaults = {
            'bucket_name': 'publicmedia',
            'custom_domain': 'publicmedia.cloudfront.net',
            'default_acl': 'public-read',
            'file_overwrite': False,
            'headers': {'Cache-Control': b'public, max-age=604800'},
            'preload_metadata': False,
            'querystring_auth': False,
            'secure_urls': True,
            'url_protocol': 'https:'}
        for key, value in defaults.items():
            kwargs.setdefault(key, value)
        return super(PublicMediaS3BotoStorage, self).__init__(*args, **kwargs)

public_media_storage = PublicMediaS3BotoStorage()
