django-varlet
=============

An implementation of models, views etc. that can act as **pages**, though they
have no content fields, depending instead of using `django-metaknight`_ to bind
them together with `django-editregions`_ into something resembling functional.

Pages all live under one flat URL namespace (eg: ``/myurlprefix/<slug>/``),
because providing any sort of page hierarchy in the URL
(eg: ``/myurlprefix/<slug>/<slug>/``) is a terrible idea as soon as you want to
move a page from one place to another.

The homepage is never accessible via it's slug, instead living at the root
of whatever URL namespace might be in use (eg: ``/myurlprefix/``)

.. _django-metaknight: https://github.com/kezabelle/django-metaknight
.. _django-editregions: https://github.com/kezabelle/django-editregions
