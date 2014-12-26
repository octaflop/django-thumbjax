# -*- coding: utf-8 -*-
import os

from django import template

from thumbjax.tasks import task_thumbnail

register = template.Library()

@register.simple_tag
def thumbjax(img, sizing, crop, *args, **kwargs):
    """
    The user-facing tag interface
    """
    width = ''
    height = ''
    if 'x' in sizing:
        width, height = sizing.split('x')
    else:
        width = sizing

    attrs = {
        'class': 'thumbj',
        'data-sizing': sizing,
        'data-crop': crop,
        'src': img.url,
        'data-img': img,
        'width': width,
        'height': height
    }
    for kw in kwargs.keys():
        attrs['data-{0}'.format(kw)] = kwargs[kw]

    # we attempt to grab a pre-cached image
    t = task_thumbnail.delay(img, sizing, crop=crop, **kwargs)
    attrs['data-taskid'] = t.id
    try:
        url = t.get(timeout=0.10)
        print "got url {0}".format(url)
        attrs['src'] = url
        # No need to grab it twice, then!
        attrs['class'] = 'thumbj-done thumbj-cached'
    except AttributeError:
        pass
    except Exception:
        pass

    attrstr = ""
    for key in attrs.keys():
        attrstr += "{0}='{1}' ".format(key, attrs[key])

    return attrstr
