# -*- coding: utf-8 -*-
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer
from zope import schema
from visaplan.plone.interfaces import IHeightAndWidth
from plone.autoform.interfaces import IFormFieldProvider

from Acquisition import aq_inner
# from visaplan.plone.animations.interfaces import ...
from plone import api
from Products.Five import BrowserView
from time import time

from visaplan.tools.debug import pp
from pdb import set_trace
from logging import getLogger
logger = getLogger(__package__+':FolderishAnimation')
from visaplan.plone.animations import _


class IFolderishAnimation(model.Schema):
    """ Marker interface for FolderishAnimation
    """
    # model/fields moved to --> IHeightAndWidth


@implementer(IFolderishAnimation, IHeightAndWidth)
class FolderishAnimation(Container):
    """
    Folderish animation type
    """


class FolderishAnimationView(BrowserView):
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
                logger.info('Ignoring %(mtype)r image %(name)s', locals())
                continue
            if mtype.endswith('javascript'):
                if timestamp is None:
                    timestamp = '?%d' % (time(),)
                logger.info('Found %(mtype)r script %(name)s', locals())
                res.append('<script type="%(mtype)s" src="%(name)s%(timestamp)s"></script>'
                           % locals())
                continue
            if mtype == 'text/css':
                logger.info('Found %(mtype)r stylesheet %(name)s', locals())
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

    def dimensions(self):
        """
        Return the given dimensions in a dict
        """
        context = aq_inner(self.context)
        field = context.Schema()
        res = {
            'height': field['height'],
            'width':  field['width'],
            }
        res['style'] = ';'.join(['%s: %dpx' % tup
                                 for tup in sorted(res.items())
                                 ])
        pp(res=res)
        return res

