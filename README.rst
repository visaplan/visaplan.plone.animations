.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

=========================
visaplan.plone.animations
=========================
.. image::
   https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336
       :target: https://pycqa.github.io/isort/

A dexterity-based content type for animations.


Features
--------

- Provides a `FolderishAnimation` content type which ...
- *contains* it's specific (Javascript, most likely) resources, while
- using more generic (library) resources, common for all animations of a common
  type, from a "global" resource path
- Currently we have exactly *one* type, tailored to our CreateJS_-based
  animations.


Examples
--------

This add-on can be seen in action at the following sites:

- https://www.unitracc.de
- https://www.unitracc.com


Documentation
-------------

Sorry, we don't have real user documentation yet.


Installation
------------

Add visaplan.plone.animations_ to your buildout_::

    [buildout]
    ...

    eggs =
        ...
        visaplan.plone.animations


and then running ``bin/buildout``; or add it to the requirements of your own
extension or policy package.

After (re-) starting your Zope instance, you'll need to "install" the
extension, using the extensions installation form or the Zope quick-installer.


Contribute
----------

- Issue Tracker: https://github.com/visaplan/visaplan.plone.animations/issues
- Source Code: https://github.com/visaplan/visaplan.plone.animations


Support
-------

If you are having issues, please let us know;
please use the `issue tracker`_ mentioned above.


License
-------

The project is licensed under the GPLv2.

.. _`CreateJS`: https://www.createjs.com
.. _`issue tracker`: https://github.com/visaplan/visaplan.plone.animations/issues
.. _visaplan.plone.animations: https://pypi.org/project/visaplan.plone.animations
.. _buildout: https://pypi.org/project/zc.buildout

.. vim: tw=79 cc=+1 sw=4 sts=4 si et
