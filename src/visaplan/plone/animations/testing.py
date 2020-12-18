# -*- coding: utf-8 -*-
# Python compatibility:
from __future__ import absolute_import

# Standard library:
import warnings

with warnings.catch_warnings():
    warnings.simplefilter('ignore', ImportWarning)

    # from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
    # Plone:
    from plone.app.testing import (
        PLONE_FIXTURE,
        FunctionalTesting,
        IntegrationTesting,
        PloneSandboxLayer,
        applyProfile,
        )
    from plone.testing import z2

# Local imports:
import visaplan.plone.animations


class VisaplanPloneAnimationsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        # Plone:
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        self.loadZCML(package=visaplan.plone.animations)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'visaplan.plone.animations:default')


VISAPLAN_PLONE_ANIMATIONS_FIXTURE = VisaplanPloneAnimationsLayer()


VISAPLAN_PLONE_ANIMATIONS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(VISAPLAN_PLONE_ANIMATIONS_FIXTURE,),
    name='VisaplanPloneAnimationsLayer:IntegrationTesting',
)


VISAPLAN_PLONE_ANIMATIONS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(VISAPLAN_PLONE_ANIMATIONS_FIXTURE,),
    name='VisaplanPloneAnimationsLayer:FunctionalTesting',
)


# VISAPLAN_PLONE_ANIMATIONS_ACCEPTANCE_TESTING = FunctionalTesting(
#     bases=(
#         VISAPLAN_PLONE_ANIMATIONS_FIXTURE,
#         REMOTE_LIBRARY_BUNDLE_FIXTURE,
#         z2.ZSERVER_FIXTURE,
#     ),
#     name='VisaplanPloneAnimationsLayer:AcceptanceTesting',
# )
