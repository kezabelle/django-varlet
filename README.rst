django-varlet
=============

:author: Keryn Knight
:version: 0.2.2

.. |travis_stable| image:: https://travis-ci.org/kezabelle/django-varlet.svg?branch=0.2.2
  :target: https://travis-ci.org/kezabelle/django-varlet

.. |travis_master| image:: https://travis-ci.org/kezabelle/django-varlet.svg?branch=master
  :target: https://travis-ci.org/kezabelle/django-varlet

==============  ======
Release         Status
==============  ======
stable (0.2.2)  |travis_stable|
master          |travis_master|
==============  ======

An implementation of models, views etc. that can act as **pages**, though they
have no content fields to speak of. Bring Your Own Content.

Pages consist only of a URL and a way to render a template at that URL. The
default model implementation uses `django-templateselector`_ to provide template
selection from HTML files within ``<templatedir>/varlet/pages/layouts``

The application uses `swapper`_ to theoretically allow for using a different
model.

If the application is mounted at the project root ``/``, Pages may not have
URLs which collide with those of another application in the urlconf.

The license
-----------

It's the `FreeBSD`_. There's should be a ``LICENSE`` file in the root of the repository, and in any archives.

.. _FreeBSD: http://en.wikipedia.org/wiki/BSD_licenses#2-clause_license_.28.22Simplified_BSD_License.22_or_.22FreeBSD_License.22.29
.. _django-templateselector: https://github.com/kezabelle/django-template-selector
.. _swapper: https://github.com/wq/django-swappable-models
