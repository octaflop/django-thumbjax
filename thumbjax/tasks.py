# -*- coding: utf-8 -*-

from sorl.thumbnail import get_thumbnail

from celery.task import task

@task()
def task_thumbnail(imgurl, sizing, **kwargs):
    im = get_thumbnail(imgurl, sizing, **kwargs)
    url = im.url
    return url
