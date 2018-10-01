# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IAnimation(model.Schema):
    """ Marker interface for Animation
    """


@implementer(IAnimation)
class Animation(Container):
    """
    """
