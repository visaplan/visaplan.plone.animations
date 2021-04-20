# -*- coding: utf-8 -*-
# Python compatibility:
from __future__ import absolute_import

from six.moves import range

# Standard library:
from cgi import escape as cgi_escape
from time import time

# Zope:
from Acquisition import aq_inner
from Products.Five import BrowserView
from zope import schema
from zope.component import getMultiAdapter, getUtility
from zope.interface import implementer
from zope.interface.interfaces import IMethod
from zope.schema import getFieldsInOrder

# Plone:
from plone import api
from plone.autoform.interfaces import IFormFieldProvider
from plone.behavior.interfaces import IBehaviorAssignable
from plone.dexterity.content import Container
from plone.dexterity.interfaces import IDexterityFTI

# visaplan:
from visaplan.plone.behaviors.interfaces import (
    ICaptionAndLegend,
    IExcludeFromSearch,
    IHeightAndWidth,
    IHierarchicalBuzzword,
    IPreviewImage,
    )
from visaplan.plone.staticthumbnails.mixin import DedicatedThumbnailMixin

# Local imports:
from ..interfaces import IFolderishAnimation

# Logging / Debugging:
from logging import getLogger
from pdb import set_trace
from visaplan.tools.debug import pp

logger = getLogger('visaplan.plone.animations:FolderishAnimation')

# Local imports:
from .. import _

__all__ = [  # public interface:
        'FolderishAnimation',          # content class
        'FolderishAnimationView',      # BrowserView
        'FolderishAnimationAjaxView',  # BrowserView w/ajax_load=1
        ]

JAVASCRIPT_MTYPE_MODES = (UNCHANGED, FORCE_TEXTUAL, FORCE_APPLICATION, REMOVE) = tuple(range(4))
JAVASCRIPT_MTYPE_MODE = FORCE_TEXTUAL
JAVASCRIPT_MTYPE_MODE = REMOVE
JS_TEXTUAL = 'text/javascript'
JS_APPLICATION = 'application/javascript'
MASK_INLINE_MTYPE = ('<script type="%(mtype)s">'
              '%(data)s'
              '</script>')
MASK_INLINE_PLAIN = ('<script>'
              '%(data)s'
              '</script>')
MASK_MTYPE = ('<script type="%(mtype)s" src="%(name)s%(timestamp)s">'
              '</script>')
MASK_PLAIN = ('<script src="%(name)s%(timestamp)s">'
              '</script>')
USE_TIMESTAMPS = True


# Is there a better way?
@implementer(IFolderishAnimation, IHeightAndWidth, ICaptionAndLegend,
             IExcludeFromSearch, IHierarchicalBuzzword,
             IPreviewImage)
class FolderishAnimation(Container, DedicatedThumbnailMixin):
    """
    Folderish animation type
    """

    def _getDefaultThumbnailPath(self):
        """
        Rückgabewert für getThumbnailPath, wenn kein spezielles
        Vorschaubild für die konkrete Animation konfiguriert
        """
        return self._buildStaticImagePath('picto_media_animation_m.png')

    # (copied from Products.unitracc.content.base)
    # quick solution, for now; we might use an indexer some day:
    def getCustomSearch(self, media=0):
        """
        Basisversion für alle von UnitraccBase abgeleiteten Typen;
        jeder Listeneintrag ist ein mögliches Suchkriterium.

        Achtung: Kommaseparierte Werte innerhalb *eines* Listenelements
                 funktionieren *nicht*!
        """
        liz = ['portal_type=' + self.portal_type]
        if media:
            mediaType, mediaFormat = self.getContentType().split('/')
            liz.append('mediaType=' + mediaType)
            liz.append('mediaFormat=' + mediaFormat)
        groupsharing = self.restrictedTraverse('@@groupsharing')
        liz.extend(groupsharing.get_custom_search_authors())
        try:
            for group_id in self.getUnitraccGroups():
                liz.append("groups=" + group_id)
        except AttributeError as e:
            logger.error('FolderishAnimation.getCustomSearch: %(e)r',
                         locals())
        return liz


def get_js_values(name, o, mtype):
    """
    Values for javascript files
    """
    inline = name.startswith('inline')
    if inline:
        data = o.data.strip().join('\n\n')
    else:
        data = None
    if JAVASCRIPT_MTYPE_MODE == REMOVE:
        if inline:
            mask = MASK_INLINE_PLAIN
        else:
            mask = MASK_PLAIN
    else:
        if inline:
            mask = MASK_INLINE_MTYPE
        else:
            mask = MASK_MTYPE
        if JAVASCRIPT_MTYPE_MODE == FORCE_TEXTUAL:
            forced_mtype = JS_TEXTUAL
        elif JAVASCRIPT_MTYPE_MODE == FORCE_APPLICATION:
            forced_mtype = JS_APPLICATION
        else:
            forced_mtype = None
        if forced_mtype is not None and mtype != forced_mtype:
            logger.info('Changing MIME type of %(name)r from %(mtype)r to %(forced_mtype)r',
                        locals())
            mtype = forced_mtype
    return (mask, inline, data, mtype)


class FolderishAnimationView(BrowserView):
    # ../templates/animation_view.pt
    # ../templates/animation_embed.pt

    def _file_elements(self):
        """
        Return a list of <script> and/or <style> elements

        Other files might still exist but are not handled by this method;
        they can be used e.g. by scripts which are loaded by a <script> element
        """
        logger.info('calling _file_elements')
        context = aq_inner(self.context)
        res = []
        if USE_TIMESTAMPS:
            timestamp = None
        else:
            timestamp = ''
        preload_img = None
        for name, o in context.items():
            mtype = o.getContentType()
            if mtype.startswith('image/'):
                if self.is_preload_img_name(name):
                    if preload_img is None:
                        preload_img = name
                        logger.info('Preloader image is %(preload_img)s',
                                    locals())
                    else:
                        logger.warn('Duplicate preloader image %(name)s'
                                    ', ignored!' , locals())
                else:
                    logger.info('Ignoring %(mtype)r image %(name)s', locals())
                continue
            if mtype.endswith('javascript'):
                logger.info('Found %(mtype)r script %(name)s', locals())
                mask, inline, data, mtype = get_js_values(name, o, mtype)
                if USE_TIMESTAMPS and not inline and timestamp is None:
                    timestamp = '?%d' % (time(),)
                res.append(mask % locals())
                continue
            if mtype == 'text/css':
                logger.info('Found %(mtype)r stylesheet %(name)s', locals())
                res.append('<link rel="stylesheet" href="%(name)s">'
                           % locals())
                continue
            logger.warn("Not creating no element for %(o)r (%(mtype)s)", locals())

        if preload_img is None:
            preload_img = self.default_preload_img_name()
        self._preload_img = preload_img
        return res

    def is_preload_img_name(self, name):
        """
        Inspect the name of an uploaded image
        """
        return (name.startswith('_preloader') or
                name.startswith('preload')
                )

    def default_preload_img_name(self):
        """
        Return the path to a default preload image
        """
        return None

    def file_names(self):
        """
        Return a list of names of the contained files

        For development purposes only
        """
        logger.info('calling file_names')
        context = aq_inner(self.context)
        return context.objectIds()

    def all_values(self):
        """
        Return a dict containing all values of all schema fields
        """
        assert isinstance(self, FolderishAnimationView)
        context = aq_inner(self.context)
        assert isinstance(context, FolderishAnimation)
        res = {}
        # https://stackoverflow.com/a/12178741/1051649:
        for name, desc in IFolderishAnimation.namesAndDescriptions():
            value = getattr(context, name, None)
            logger.info('.all_values %(name)r: %(desc)s', locals())
            if IMethod.providedBy(desc):
                logger.info('%(name)s: a method', locals())
                # It's a method --> call it:
                value = value()
            res[name] = value
        try:
            name = 'FolderishAnimation'
            schema = getUtility(IDexterityFTI, name=name).lookupSchema()
            logger.info('schema is %(schema)r', locals())
        except Exception as e:
            logger.exception(e)
            logger.error('Could not get schema for name %(name)r', locals())

        behavior_assignable = IBehaviorAssignable(context)
        if behavior_assignable:
            first = 1
            for behavior in behavior_assignable.enumerateBehaviors():
                logger.info('behavior: %(behavior)r', locals())
                for name, field in getFieldsInOrder(behavior.interface):
                    if name == 'subjects':
                        continue
                    try:
                        value = field.get(context)
                        if callable(value):
                            value = value()
                        res[name] = value
                        logger.info('  %(name)r --> %(value)r', locals())
                    except Exception as e:
                        # XXX Access to the fields from my behaviors doesn't work!
                        logger.exception(e)
                        logger.error('name=%(name)r, field=%(field)r', locals())
                        set_trace()
                        value = field.get(context)
                        if callable(value):
                            value = value()
                        res[name] = value
        if 'height' in res and 'width' in res:
            res['_calculated'] = {
                'style': ';'.join(['%s:%spx' % (k, res[k])
                                   for k in ('height', 'width')
                                   ]),
                }
            logger.info('style=%(style)s', res['_calculated'])
        pp(res)
        res['file_elements'] = self._file_elements()
        res['preload_img'] = self._preload_img

        scales = getMultiAdapter((context, context.REQUEST), name='images')
        scale = scales.scale('image', scale='preview')
        if scale:
            res['preview_image_tag'] = scale.tag(title=None,
                            alt=_('Open a new window to start the animation'))
        else:
            res['preview_image_tag'] = self._clickable_text()
            logger.warn('No preview image found for %(context)r', locals())
        return res

    def _clickable_text(self):
        """
        The "clickability" is provided by the enclosing <a> element
        """
        hint = _('Open a new window to start the animation')
	title = _('Sorry, no preview image (yet)!')
        return (u'<span title="' + cgi_escape(title, True) + u'">'
                + cgi_escape(hint)
                + u'</span>')


class FolderishAnimationAjaxView(FolderishAnimationView):
    def __init__(self, context, request):
        FolderishAnimationView.__init__(self, context, request)
        request.set('ajax_load', 1)
