# -*- coding: utf-8 -*-

import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

class ThumbnailStorage(FileSystemStorage):
    def __init__(self, **kwargs):
        super(ThumbnailStorage, self).__init__(
            location=settings.THUMBNAIL_DEBUG_PATH,
            base_url=settings.THUMBNAIL_DEBUG_URL)
