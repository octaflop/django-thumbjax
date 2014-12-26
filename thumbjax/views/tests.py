# -*- coding: utf-8 -*-

import os
import random

from django.shortcuts import render
from django.utils.http import int_to_base36
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings
from zaneprep.generic import login_required

from users.decorators import campus_manager_required
from team.models import TeamMember


def _get_test_imgs():
    test_imgs = []
    for team in TeamMember.objects.all():
        test_imgs.append(team.profile_picture)
    return test_imgs


@login_required
@campus_manager_required
def index(request):
    ctx = {}
    template_name = 'thumbjax/tests/index.html'
    return render(request, template_name, ctx)


@login_required
@campus_manager_required
def control_group(request):
    ctx = {}
    ctx['test_images'] = _get_test_imgs()
    template_name = 'thumbjax/tests/control_group.html'
    return render(request, template_name, ctx)


@login_required
@campus_manager_required
def std_thumbnailer(request):
    ctx = {}
    test_images = _get_test_imgs()
    ctx['test_images'] = test_images
    template_name = 'thumbjax/tests/std_thumbnailer.html'
    return render(request, template_name, ctx)


@login_required
@campus_manager_required
def thumbjaxd(request):
    ctx = {}
    test_images = _get_test_imgs()
    ctx['test_images'] = test_images
    template_name = 'thumbjax/tests/thumbjaxd.html'
    return render(request, template_name, ctx)
