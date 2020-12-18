# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

# Python compatibility:
from __future__ import absolute_import

# Zope:
from zope import schema
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

# Plone:
from plone.supermodel import model

# Local imports:
from visaplan.plone.animations import _


class IFolderishAnimation(model.Schema):
    """ Marker interface for FolderishAnimation
    """
    model.fieldset(
	u"basic",
	label=_(u"Basic"),
	fields=['type_nr',
		])

    type_nr = schema.Int(
        title=_(u"Type number"),
        default=1,
        required=True,
        description=_(u"The implementation of folderish animations might "
            u'evolve, and some of the improvents might be incompatible to '
            u'older animation objects.'))
    # other model/fields moved to --> IHeightAndWidth


class IVisaplanPloneAnimationsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
