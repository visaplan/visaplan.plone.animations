from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass

from Products.CMFCore.ActionInformation import ActionInfo
from Products.CMFCore.interfaces import IAction

from Products.CMFPlone.PloneBaseTool import PloneBaseTool


class AnimationsTool(PloneBaseTool):

    meta_type = 'Plone Animations Tool'
    security = ClassSecurityInfo()
    toolicon = 'skins/plone_images/document_icon.png'
