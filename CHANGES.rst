Changelog
=========


1.0.5 (2021-02-16)
------------------

New Features:

- `FolderishAnimation.getCustomSearch` method, providing (for now):

  - portal_type
  - Creator

Profile changes:

- Upgrade step to update the ``getCustomSearch`` indexes
- Profile version increased to 1002

[tobiasherp]


1.1 (2021-02-16)
----------------

- CreateJS-based "Type 2", using `class` instead of `id` attributes

[tobiasherp]


1.0.4 (2020-12-16)
------------------

Improvements:

- Made FolderishAnimations clickable even if lacking a preview image

[tobiasherp]


1.0.3 (2020-03-05)
------------------

- Views for AJAX navigation support (based on visaplan.plone.ajaxnavigation_)
- Added an ``ajax-nav`` view to prevent Plone from trying to load a FolderishAnimation via AJAX
  (since this doesn't work yet).
- Since it is not usable as an AJAX navigation target,
  the ``embed`` view has been renamed to ``onlyme``

[tobiasherp]


1.0.2 (2019-10-22)
------------------

- Removed profile dependency on visaplan.plone.behaviors, since the current version 1.0.2 doesn't have one.

[tobiasherp]


1.0.1 (2019-06-26)
------------------

- Support for preloader images, recognized by name
- use visaplan.plone.staticthumbnails_
- Add CSS classes to HTML text

[tobiasherp]


1.0 (2019-05-20)
----------------

- Initial release.
  [tobiasherp]

.. _visaplan.plone.ajaxnavigation: https://pypi.org/project/visaplan.plone.ajaxnavigation
.. _visaplan.plone.staticthumbnails: https://pypi.org/project/visaplan.plone.staticthumbnails
