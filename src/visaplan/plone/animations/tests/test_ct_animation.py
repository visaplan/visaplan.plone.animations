# -*- coding: utf-8 -*-
from visaplan.plone.animations.content.animation import IAnimation  # NOQA E501
from visaplan.plone.animations.testing import VISAPLAN_PLONE_ANIMATIONS_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


try:
    from plone.dexterity.schema import portalTypeToSchemaName
except ImportError:
    # Plone < 5
    from plone.dexterity.utils import portalTypeToSchemaName


class AnimationIntegrationTest(unittest.TestCase):

    layer = VISAPLAN_PLONE_ANIMATIONS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_ct_animation_schema(self):
        fti = queryUtility(IDexterityFTI, name='Animation')
        schema = fti.lookupSchema()
        schema_name = portalTypeToSchemaName('Animation')
        self.assertEqual(schema_name, schema.getName())

    def test_ct_animation_fti(self):
        fti = queryUtility(IDexterityFTI, name='Animation')
        self.assertTrue(fti)

    def test_ct_animation_factory(self):
        fti = queryUtility(IDexterityFTI, name='Animation')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            IAnimation.providedBy(obj),
            u'IAnimation not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_animation_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='Animation',
            id='animation',
        )

        self.assertTrue(
            IAnimation.providedBy(obj),
            u'IAnimation not provided by {0}!'.format(
                obj.id,
            ),
        )

    def test_ct_animation_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Animation')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_animation_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='Animation')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'animation_id',
            title='Animation container',
         )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
