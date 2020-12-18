# -*- coding: utf-8 -*-
# Python compatibility:
from __future__ import absolute_import

# Plone:
from plone.app.upgrade.utils import loadMigrationProfile


def reload_gs_profile(context):
    loadMigrationProfile(
        context,
        'profile-visaplan.plone.animations:default',
    )
