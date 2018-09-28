# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from visaplan.plone.animations.testing import VISAPLAN_PLONE_ANIMATIONS_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that visaplan.plone.animations is properly installed."""

    layer = VISAPLAN_PLONE_ANIMATIONS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if visaplan.plone.animations is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'visaplan.plone.animations'))

    def test_browserlayer(self):
        """Test that IVisaplanPloneAnimationsLayer is registered."""
        from visaplan.plone.animations.interfaces import (
            IVisaplanPloneAnimationsLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IVisaplanPloneAnimationsLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = VISAPLAN_PLONE_ANIMATIONS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['visaplan.plone.animations'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if visaplan.plone.animations is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'visaplan.plone.animations'))

    def test_browserlayer_removed(self):
        """Test that IVisaplanPloneAnimationsLayer is removed."""
        from visaplan.plone.animations.interfaces import \
            IVisaplanPloneAnimationsLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IVisaplanPloneAnimationsLayer,
            utils.registered_layers())
