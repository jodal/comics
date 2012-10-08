***********
Web service
***********

*comics* comes with a web service that exposes all useful data about the
current user, comics, comic releases, and comic images. The web service may be
used to e.g. create iOS/Android apps or alternative comics browsers, while
leaving the comics crawling job to a *comics* instance.

Please make any apps using this API generic, so that they can be used with any
*comics* instance as the backend. In other words, please let the end user
enter the hostname of the *comics* instance himself.


Authentication
==============

The web service is only available for users with an active user account on the
*comics* instance. The user must authenticate himself using the same
secret key as is used to access comic feeds. The secret key can be provided in
one of two ways:

- Using a HTTP GET parameter named ``key``, i.e. as part of the URL. Example::

      http://example.com/api/v1/user/?key=76acdcdf16ae4e12becb00d09a9d9456

- Using the ``Authorization`` HTTP header. Example::

      Authorization: Key 76acdcdf16ae4e12becb00d09a9d9456


Response format
===============

You can specify the wanted response format in one of two ways:

- Using a HTTP GET parameter named ``format``, i.e. as part of the URL.
  Examples::

      # Returns JSON
      http://example.com/api/v1/?format=json

      # Returns JSONP with function name 'callback'
      http://example.com/api/v1/?format=jsonp

      # Returns JSONP with function name 'foo'
      http://example.com/api/v1/?format=jsonp&callback=foo

      # Returns JSONP with function name 'foo'
      http://example.com/api/v1/?callback=foo

      # Returns XML
      http://example.com/api/v1/?format=xml

      # Returns YAML
      http://example.com/api/v1/?format=yaml

      # Returns Apple binary plist
      http://example.com/api/v1/?format=plist

- Using the ``Accept`` HTTP header. Examples::

      # Returns JSON
      Accept: application/json

      # Returns JSONP with function name 'callback'
      Accept: text/javascript

      # Returns XML
      Accept: application/xml

      # Returns YAML
      Accept: text/yaml

      # Returns Apple binary plist
      Accept: application/x-plist

JSON and JSONP are always supported. Other formats like XML, YAML, and Apple
binary plists (bplist) may be available if the *comics* instance got the
additional dependencies required by the format installed.

If you run a *comics* instance yourself, and want support for more response
formats, check out `Tastypie's serialization docs
<http://django-tastypie.readthedocs.org/en/latest/serialization.html>`_ for
details on what you need to install.


Resources
=========

.. http:get:: /api/v1/

    List all available resources, and URLs for their schemas.

.. http:get:: /api/v1/user/

    Get the authenticated user.

    **Example request**

    .. sourcecode:: http

        GET /api/v1/user/ HTTP/1.1
        Host: example.com
        Accept: application/json
        Authorization: Key 76acdcdf16ae4e12becb00d09a9d9456

    **Example response**

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json; charset=utf-8

        {
            meta: {
                limit: 20,
                next: null,
                offset: 0,
                previous: null,
                total_count: 1
            },
            objects: [
                {
                    date_joined: "2012-04-30T18:39:59+00:00",
                    email: "alice@example.com",
                    last_login: "2012-06-09T23:09:54.312109+00:00",
                    resource_uri: "/api/v1/user/1/",
                    secret_key: "76acdcdf16ae4e12becb00d09a9d9456"
                }
            ]
        }

    :statuscode 200: no error
    :statuscode 401: authorization failed

.. http:get:: /api/v1/comics/

    Lists all available comics.

    **Example request**

    .. sourcecode:: http

        TODO

    **Example response**

    .. sourcecode:: http

        TODO

    :query my: only include comics in "my comics" if ``true``

.. http:get:: /api/v1/releases/

    Lists all available releases, last fetched first.

    **Example request**

    .. sourcecode:: http

        TODO

    **Example response**

    .. sourcecode:: http

        TODO

    :query my: only include releases from "my comics" if ``true``

.. http:get:: /api/v1/images/

    Lists all images. You'll probably not use this one, as the images are
    available through the ``releases`` resource as well.
