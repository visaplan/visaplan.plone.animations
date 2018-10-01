# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s visaplan.plone.animations -t test_animation.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src visaplan.plone.animations.testing.VISAPLAN_PLONE_ANIMATIONS_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/visaplan/plone/animations/tests/robot/test_animation.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Animation
  Given a logged-in site administrator
    and an add Animation form
   When I type 'My Animation' into the title field
    and I submit the form
   Then a Animation with the title 'My Animation' has been created

Scenario: As a site administrator I can view a Animation
  Given a logged-in site administrator
    and a Animation 'My Animation'
   When I go to the Animation view
   Then I can see the Animation title 'My Animation'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Animation form
  Go To  ${PLONE_URL}/++add++Animation

a Animation 'My Animation'
  Create content  type=Animation  id=my-animation  title=My Animation

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Animation view
  Go To  ${PLONE_URL}/my-animation
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Animation with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Animation title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
