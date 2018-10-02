# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer

from Acquisition import aq_inner
# from visaplan.plone.animations.interfaces import ...
from plone import api
from Products.Five import BrowserView
from time import time

from visaplan.tools.debug import pp
from pdb import set_trace
from logging import getLogger
logger = getLogger(__package__+'.Animation')


class IAnimation(model.Schema):
    """ Marker interface for Animation
    """


@implementer(IAnimation)
class Animation(Container):
    """
    Folderish Animation type
    """


class AnimationView(BrowserView):
    # ../templates/animation_view.pt
    
    def file_elements(self):
        """
        Return a list of <script> and/or <style> elements

        Other files might still exist but are not handled by this method;
        they can be used e.g. by scripts which are loaded by a <script> element
        """
        logger.info('calling file_elements')
        context = aq_inner(self.context)
        res = []
        timestamp = None
        for name, o in context.items():
            mtype = o.getContentType()
            if mtype.startswith('image/'):
                continue
            if mtype.endswith('javascript'):
                if timestamp is None:
                    timestamp = '?%d' % (time(),)
                res.append('<script type="%(mtype)s" src="%(name)s%(timestamp)s"></script>'
                           % locals())
                continue
            if mtype == 'text/css':
                res.append('<link rel="stylesheet" href="%(name)s">'
                           % locals())
                continue
            logger.warn("Not creating no element for %(o)r (%(mtype)s)", locals())

        return res
            

    def file_names(self):
        """
        Return a list of names of the contained files

        For development purposes only
        """
        logger.info('calling file_names')
        context = aq_inner(self.context)
        return context.objectIds()

