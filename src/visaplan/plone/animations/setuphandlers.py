# -*- coding: utf-8 -*-
# Python compatibility:
from __future__ import absolute_import

# Zope:
from zope.interface import implementer

# Plone:
from Products.CMFPlone.interfaces import INonInstallable


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'visaplan.plone.animations:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
