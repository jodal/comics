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


.. _pagination:

Pagination
==========

All the resource collections support pagination. The pagination parameters that
may be passed as :http:method:`GET` arguments are:

- **limit** -- max number of returned resources per response. Defaults to 20.

- **offset** -- offset into the full collection of resources. Defaults to 0.

The ``meta`` section of the collection responses include the current pagination
parameters, and--if available--links to the previous and next page, and the
total count of resources matching the query:

- **next** -- link to the next page of the collection, if available

- **previous** -- link to the previous page of the collection, if available

- **total_count** -- total number of resources in the collection, given the
  current filters.


Resources
=========

Root resource
-------------

.. http:get:: /api/v1/

    Lists all available resources, and URLs for their schemas.


User resource
-------------

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
    :statuscode 401: authentication/authorization failed


Comics resource
---------------

.. http:get:: /api/v1/comics/

    Lists all available comics. Supports :ref:`pagination`.

    **Example request**

    .. sourcecode:: http

        GET /api/v1/comics/?slug=xkcd HTTP/1.1
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
                    active: true,
                    added: "0001-01-01T00:00:00+00:00",
                    end_date: null,
                    id: "18",
                    language: "en",
                    name: "xkcd",
                    resource_uri: "/api/v1/comics/18/",
                    rights: "Randall Munroe, CC BY-NC 2.5",
                    slug: "xkcd",
                    start_date: "2005-05-29",
                    url: "http://www.xkcd.com/"
                }
            ]
        }

    :query subscribed: only include comics the authorized user is subscribed to
        if ``true``, or unsubscribed to if ``false``
    :query active: only include active comics (``true``) or inactive comics
        (``false``)
    :query language: only include comics with the exact language, e.g. ``en``
    :query name: only include comics with matching name. Queries like
        ``name__startswith=Dilbert`` and ``name__iexact=XkcD`` are supported.
    :query slug: only include comics with matching slug. Queries like
        ``slug__contains=kc`` and ``slug__endswith=db`` are supported.

    :statuscode 200: no error
    :statuscode 400: bad request, e.g. unknown filter used
    :statuscode 401: authentication/authorization failed

.. http:get:: /api/v1/comics/(int:comic_id)/

    Show a specific comic looked up by comic ID.

    **Example request**

    .. sourcecode:: http

        GET /api/v1/comics/18/ HTTP/1.1
        Host: example.com
        Accept: application/json
        Authorization: Key 76acdcdf16ae4e12becb00d09a9d9456

    **Example response**

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json; charset=utf-8

        {
            active: true,
            added: "0001-01-01T00:00:00+00:00",
            end_date: null,
            id: "18",
            language: "en",
            name: "xkcd",
            resource_uri: "/api/v1/comics/18/",
            rights: "Randall Munroe, CC BY-NC 2.5",
            slug: "xkcd",
            start_date: "2005-05-29",
            url: "http://www.xkcd.com/"
        }

    :param comic_id: the comic ID

    :statuscode 200: no error
    :statuscode 401: authentication/authorization failed
    :statuscode 404: comic not found


Releases resource
-----------------

.. http:get:: /api/v1/releases/

    Lists all available releases, last fetched first. Supports
    :ref:`pagination`.

    **Example request**

    .. sourcecode:: http

        GET /api/v1/releases/?comic__slug=xkcd&limit=2 HTTP/1.1
        Host: example.com
        Accept: application/json
        Authorization: Key 76acdcdf16ae4e12becb00d09a9d9456

    **Example response**

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json; charset=utf-8

        {
            meta: {
                limit: 2,
                next: "/api/v1/releases/?limit=2&key=76acdcdf16ae4e12becb00d09a9d9456&format=json&comic__slug=xkcd&offset=2",
                offset: 0,
                previous: null,
                total_count: 1104
            },
            objects: [
                {
                    comic: "/api/v1/comics/18/",
                    fetched: "2012-10-08T04:03:56.411028+00:00",
                    id: "147708",
                    images: [
                        {
                            checksum: "605d9a6d415676a21ee286fe2b369f58db62c397bfdfa18710b96dcbbcc4df12",
                            fetched: "2012-10-08T04:03:56.406586+00:00",
                            file: "https://static.example.com/media/xkcd/6/605d9a6d415676a21ee286fe2b369f58db62c397bfdfa18710b96dcbbcc4df12.png",
                            height: 365,
                            id: "151937",
                            resource_uri: "/api/v1/images/151937/",
                            text: "Facebook, Apple, and Google all got away with their monopolist power grabs because they don't have any 'S's in their names for critics to snarkily replace with '$'s.",
                            title: "Microsoft",
                            width: 278
                        }
                    ],
                    pub_date: "2012-10-08",
                    resource_uri: "/api/v1/releases/147708/"
                },
                {
                    comic: "/api/v1/comics/18/",
                    fetched: "2012-10-05T05:03:33.744355+00:00",
                    id: "147172",
                    images: [
                        {
                            checksum: "6d1b67d3dc00d362ddb5b5e8f1c3f174926d2998ca497e8737ff8b74e7100997",
                            fetched: "2012-10-05T05:03:33.737231+00:00",
                            file: "https://static.example.com/media/xkcd/6/6d1b67d3dc00d362ddb5b5e8f1c3f174926d2998ca497e8737ff8b74e7100997.png",
                            height: 254,
                            id: "151394",
                            resource_uri: "/api/v1/images/151394/",
                            text: "According to my mom, my first word was (looking up at the sky) 'Wow!'",
                            title: "My Sky",
                            width: 713
                        }
                    ],
                    pub_date: "2012-10-05",
                    resource_uri: "/api/v1/releases/147172/"
                }
            ]
        }

    :query subscribed: only include releases the authorized user is subscribed
        to if ``true``, or unsubscribed to if ``false``
    :query comic: only include releases with matching comic. All filters on the
        comic resource may be used, e.g. ``comic__slug=xkcd``.
    :query images: only include releases with matching image. All filters on
        the image resource may be used, e.g. ``images__height__gt=1000``.
    :query pub_date: only include releases with pub_date matching. Date range
        queries, like ``pub_date__year=2011`` or
        ``pub_date__gte=2011-01-01&pub_date__lte=2011-12-31``, are supported.
    :query fetched: only include releases with fetched matching. Date range
        queries are supported.

    :statuscode 200: no error
    :statuscode 400: bad request, e.g. unknown filter used
    :statuscode 401: authentication/authorization failed

.. http:get:: /api/v1/releases/(int:release_id)/

    Show a specific release looked up by release ID.

    **Example request**

    .. sourcecode:: http

        GET /api/v1/releases/147708/ HTTP/1.1
        Host: example.com
        Accept: application/json
        Authorization: Key 76acdcdf16ae4e12becb00d09a9d9456

    **Example response**

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json; charset=utf-8

        {
            comic: "/api/v1/comics/18/",
            fetched: "2012-10-08T04:03:56.411028+00:00",
            id: "147708",
            images: [
                {
                    checksum: "605d9a6d415676a21ee286fe2b369f58db62c397bfdfa18710b96dcbbcc4df12",
                    fetched: "2012-10-08T04:03:56.406586+00:00",
                    file: "https://static.example.com/media/xkcd/6/605d9a6d415676a21ee286fe2b369f58db62c397bfdfa18710b96dcbbcc4df12.png",
                    height: 365,
                    id: "151937",
                    resource_uri: "/api/v1/images/151937/",
                    text: "Facebook, Apple, and Google all got away with their monopolist power grabs because they don't have any 'S's in their names for critics to snarkily replace with '$'s.",
                    title: "Microsoft",
                    width: 278
                }
            ],
            pub_date: "2012-10-08",
            resource_uri: "/api/v1/releases/147708/"
        }

    :param release_id: the release ID

    :statuscode 200: no error
    :statuscode 401: authentication/authorization failed
    :statuscode 404: release not found


Images resource
---------------

You will probably not use the images resource, as the images are available
through the ``releases`` resource as well. The images resource is included to
give the images referenced to by releases their own canonical URLs.

.. http:get:: /api/v1/images/

    Lists all images. Supports :ref:`pagination`.

    :query fetched: only include images with fetched matching. Date range
        queries are supported.
    :query title: only include images with matching title. Queries like
        ``title__icontains=cake`` are supported.
    :query text: only include images with matching text. Queries like
        ``text__icontains=lies`` are supported.
    :query height: only include images with height matching. Integer range
        queries, like ``height__gt=1000`` are supported.
    :query width: only include images with width matching. Integer range
        queries are supported.

    :statuscode 200: no error
    :statuscode 400: bad request, e.g. unknown filter used
    :statuscode 401: authentication/authorization failed


.. http:get:: /api/v1/images/(int:image_id)/

    Show a specific image looked up by image ID.

    :param image_id: the image ID

    :statuscode 200: no error
    :statuscode 401: authentication/authorization failed
    :statuscode 404: image not found


Subscriptions resource
----------------------

.. http:get:: /api/v1/subscriptions/

    List all the authenticated user's comic subscriptions. Supports
    :ref:`pagination`.

    **Example request**

    .. sourcecode:: http

        GET /api/v1/subscriptions/?comic__slug=xkcd HTTP/1.1
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
                    comic: "/api/v1/comics/18/",
                    id: "2",
                    resource_uri: "/api/v1/subscriptions/2/"
                }
            ]
        }

    :query comic: only include releases with matching comic. All filters on the
        comic resource may be used, e.g. ``comic__slug=xkcd``.

    :statuscode 200: no error
    :statuscode 401: authentication/authorization failed

.. http:post:: /api/v1/subscriptions/

    Subscribe the authenticated user to the given comic.

    **Example request**

    Note that the request specifies the ``Content-Type`` since it includes a
    body with JSON.

    .. sourcecode:: http

        POST /api/v1/subscriptions/ HTTP/1.1
        Host: example.com
        Accept: application/json
        Authorization: Key 76acdcdf16ae4e12becb00d09a9d9456
        Content-Type: application/json

        {
            "comic": "/api/v1/comics/18/"
        }

    **Example response**

    .. sourcecode:: http

        HTTP/1.0 201 CREATED
        Content-Type: text/html; charset=utf-8
        Location: https://example.com/api/v1/subscriptions/4/

    :statuscode 201: no error, object was created, see ``Location`` header
    :statuscode 401: authentication/authorization failed
    :statuscode 500: if the request cannot be processed, e.g. because the
        subscription already exists

.. http:get:: /api/v1/subscriptions/(int:subscription_id)/

    Show one of the authenticated user's comic subscriptions looked up by
    subscription ID.

    **Example request**

    .. sourcecode:: http

        GET /api/v1/subscriptions/2/ HTTP/1.1
        Host: example.com
        Accept: application/json
        Authorization: Key 76acdcdf16ae4e12becb00d09a9d9456

    **Example response**

    .. sourcecode:: http

        HTTP/1.0 200 OK
        Content-Type: application/json; charset=utf-8

        {
            comic: "/api/v1/comics/18/",
            id: "2",
            resource_uri: "/api/v1/subscriptions/2/"
        }

    :param subscription_id: the subscription ID

    :statuscode 200: no error
    :statuscode 401: authentication/authorization failed
    :statuscode 404: subscription not found

.. http:delete:: /api/v1/subscriptions/(int:subscription_id)

    Unsubscribe the authenticated user from the given comic.

    **Example request**

    .. sourcecode:: http

        DELETE /api/v1/subscriptions/17/ HTTP/1.1
        Host: example.com
        Accept: application/json
        Authorization: Key 76acdcdf16ae4e12becb00d09a9d9456

    **Example response**

    .. sourcecode:: http

        HTTP/1.0 204 NO CONTENT
        Content-Length: 0
        Content-Type: text/html; charset=utf-8

    :param subscription_id: the subscription ID

    :statuscode 204: no error, and no content returned
    :statuscode 401: authentication/authorization failed
    :statuscode 404: subscription not found
