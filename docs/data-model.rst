**********
Data model
**********

Comics' data model is quite simple:

- The :mod:`comics.core` app consists of three models;
  :class:`~comics.core.models.Comic`, :class:`~comics.core.models.Release`, and
  :class:`~comics.core.models.Image`.

- The :mod:`comics.accounts` app adds a
  :class:`~comics.accounts.models.UserProfile` which add comic specific
  fields to Django's user model, including a mapping from the user to her
  preferred comics.

.. image:: _static/data_model.png


Database migrations
===================

Changes to the data model are managed using Django's `database migrations
<https://docs.djangoproject.com/en/1.11/topics/migrations/>`_. If you need to
change the models, please provide the needed migrations.


Updating diagram
================

The above data model diagram was generated using the Django app
`django-extensions <https://github.com/django-extensions/django-extensions>`_ and
the following command:

.. code-block:: sh

    uv run comics graph_models \
      --output docs/_static/data_model.png \
      --group-models \
      core accounts
