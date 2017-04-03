import base64
import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from comics.accounts.models import Subscription
from comics.core.models import Comic


def create_user():
    user = User.objects.create_user('alice', 'alice@example.com', 'secret')
    user.comics_profile.secret_key = 's3cretk3y'
    user.comics_profile.save()
    return user


def create_subscriptions(user):
    Subscription.objects.create(
        userprofile=user.comics_profile,
        comic=Comic.objects.get(slug='geekandpoke'))
    Subscription.objects.create(
        userprofile=user.comics_profile,
        comic=Comic.objects.get(slug='xkcd'))


class RootResourceTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_root_without_authentication(self):
        response = self.client.get('/api/v1/')

        self.assertEquals(response.status_code, 200)

    def test_root_resource_returns_other_resource_endpoints_in_json(self):
        response = self.client.get('/api/v1/')

        data = json.loads(response.content)
        self.assertIn('comics', data)
        self.assertEquals(data['users']['list_endpoint'], '/api/v1/users/')
        self.assertEquals(data['comics']['list_endpoint'], '/api/v1/comics/')
        self.assertEquals(data['images']['list_endpoint'], '/api/v1/images/')
        self.assertEquals(
            data['releases']['list_endpoint'], '/api/v1/releases/')
        self.assertEquals(
            data['subscriptions']['list_endpoint'], '/api/v1/subscriptions/')

    def test_resource_can_return_xml(self):
        response = self.client.get('/api/v1/', HTTP_ACCEPT='application/xml')

        self.assertIn(
            "<?xml version='1.0' encoding='utf-8'?>", response.content)

    def test_resource_can_return_jsonp(self):
        response = self.client.get('/api/v1/', {'format': 'jsonp'})

        self.assertIn('callback(', response.content)

    def test_resource_can_return_jsonp_with_custom_callback_name(self):
        response = self.client.get(
            '/api/v1/', {'format': 'jsonp', 'callback': 'foo'})

        self.assertIn('foo(', response.content)

    def test_resource_returns_jsonp_if_just_given_callback_name(self):
        response = self.client.get('/api/v1/', {'callback': 'foo'})

        self.assertIn('foo(', response.content)


class UsersResourceTestCase(TestCase):
    def setUp(self):
        create_user()
        self.client = Client()

    def test_get_users_without_authentication(self):
        response = self.client.get('/api/v1/users/')

        self.assertEquals(response.status_code, 401)

    def test_get_users_with_basic_auth(self):
        response = self.client.get(
            '/api/v1/users/',
            HTTP_AUTHORIZATION='Basic %s' %
            base64.encodestring('alice:secret'))

        self.assertEquals(response.status_code, 200)

    def test_get_users_with_secret_key_in_header(self):
        response = self.client.get(
            '/api/v1/users/', HTTP_AUTHORIZATION='Key s3cretk3y')

        self.assertEquals(response.status_code, 200)

    def test_get_users_with_secret_key_in_url(self):
        response = self.client.get(
            '/api/v1/users/', {'key': 's3cretk3y'})

        self.assertEquals(response.status_code, 200)

    def test_response_returns_a_single_user_object(self):
        User.objects.create_user('bob', 'bob@example.com', 'topsecret')

        response = self.client.get(
            '/api/v1/users/', HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 1)

    def test_response_includes_the_secret_key(self):
        response = self.client.get(
            '/api/v1/users/', HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(data['objects'][0]['secret_key'], 's3cretk3y')


class ComicsResourceTestCase(TestCase):
    fixtures = ['comics.json']

    def setUp(self):
        self.user = create_user()
        self.client = Client()

    def test_requires_authentication(self):
        response = self.client.get('/api/v1/comics/')

        self.assertEquals(response.status_code, 401)

    def test_authentication_with_secret_key_in_header(self):
        response = self.client.get(
            '/api/v1/comics/', HTTP_AUTHORIZATION='Key s3cretk3y')

        self.assertEquals(response.status_code, 200)

    def test_lists_comics(self):
        response = self.client.get(
            '/api/v1/comics/', HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 10)
        self.assertEquals(data['objects'][0]['slug'], 'abstrusegoose')

    def test_slug_filter(self):
        response = self.client.get(
            '/api/v1/comics/', {'slug': 'xkcd'},
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 1)
        self.assertEquals(data['objects'][0]['slug'], 'xkcd')

    def test_subscribed_filter(self):
        create_subscriptions(self.user)

        response = self.client.get(
            '/api/v1/comics/', {'subscribed': 'true'},
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 2)
        self.assertEquals(data['objects'][0]['slug'], 'geekandpoke')
        self.assertEquals(data['objects'][1]['slug'], 'xkcd')

    def test_unsubscribed_filter(self):
        create_subscriptions(self.user)

        response = self.client.get(
            '/api/v1/comics/', {'subscribed': 'false'},
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 8)
        self.assertEquals(data['objects'][0]['slug'], 'abstrusegoose')

    def test_details_view(self):
        response = self.client.get(
            '/api/v1/comics/', HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        comic_uri = data['objects'][0]['resource_uri']
        self.assertEquals(comic_uri, '/api/v1/comics/1/')

        response = self.client.get(
            comic_uri, HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(data['slug'], 'abstrusegoose')


class ImagesResourceTestCase(TestCase):
    fixtures = ['comics.json']

    def setUp(self):
        create_user()
        self.client = Client()

    def test_requires_authentication(self):
        response = self.client.get('/api/v1/images/')

        self.assertEquals(response.status_code, 401)

    def test_authentication_with_secret_key_in_header(self):
        response = self.client.get(
            '/api/v1/images/', HTTP_AUTHORIZATION='Key s3cretk3y')

        self.assertEquals(response.status_code, 200)

    def test_lists_images(self):
        response = self.client.get(
            '/api/v1/images/', HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 12)
        self.assertEquals(data['objects'][0]['height'], 1132)
        self.assertEquals(
            data['objects'][1]['title'],
            "Geek&Poke About The Good Ol' Days In Computers")

    def test_height_filter(self):
        response = self.client.get(
            '/api/v1/images/', {'height__gt': 1100},
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 2)
        self.assertEquals(data['objects'][0]['height'], 1132)
        self.assertEquals(data['objects'][1]['height'], 1132)

    def test_details_view(self):
        response = self.client.get(
            '/api/v1/images/', HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        image_uri = data['objects'][1]['resource_uri']
        self.assertEquals(image_uri, '/api/v1/images/2/')

        response = self.client.get(
            image_uri, HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(
            data['title'], "Geek&Poke About The Good Ol' Days In Computers")


class ReleasesResourceTestCase(TestCase):
    fixtures = ['comics.json']

    def setUp(self):
        self.user = create_user()
        self.client = Client()

    def test_requires_authentication(self):
        response = self.client.get('/api/v1/releases/')

        self.assertEquals(response.status_code, 401)

    def test_authentication_with_secret_key_in_header(self):
        response = self.client.get(
            '/api/v1/releases/', HTTP_AUTHORIZATION='Key s3cretk3y')

        self.assertEquals(response.status_code, 200)

    def test_list_releases(self):
        response = self.client.get(
            '/api/v1/releases/', HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 11)

        release = data['objects'][0]
        self.assertEquals(release['comic'], '/api/v1/comics/9/')
        self.assertEquals(release['pub_date'], '2012-10-12')
        self.assertEquals(
            release['resource_uri'], '/api/v1/releases/11/')
        self.assertEquals(len(release['images']), 1)

        image = release['images'][0]
        self.assertEquals(image['title'], 'Blurring the Line')
        self.assertEquals(
            image['text'], 'People into masturbatory ' +
            'navel-gazing have a lot to learn about masturbation.')
        self.assertEquals(image['height'], 235)
        self.assertEquals(image['width'], 740)
        self.assertEquals(
            image['checksum'],
            '76a1407a2730b000d51ccf764c689c8930fdd3580e01f62f70cbe73d8be17e9c')

    def test_subscribed_filter(self):
        create_subscriptions(self.user)

        response = self.client.get(
            '/api/v1/releases/', {'subscribed': 'true'},
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 6)

    def test_comic_filter(self):
        response = self.client.get(
            '/api/v1/releases/', {'comic__slug': 'geekandpoke'},
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 2)

        release = data['objects'][0]
        self.assertEquals(release['comic'], '/api/v1/comics/4/')

    def test_pub_date_filter(self):
        response = self.client.get(
            '/api/v1/releases/',
            {'pub_date__year': 2012, 'pub_date__month': 10},
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 11)

        response = self.client.get(
            '/api/v1/releases/',
            {'pub_date__year': 2012, 'pub_date__month': 9},
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 0)

    def test_unknown_filter_fails(self):
        response = self.client.get(
            '/api/v1/releases/',
            {'pub_date__foo': 'bar'},
            HTTP_AUTHORIZATION='Key s3cretk3y')

        self.assertEquals(response.status_code, 400)

    def test_details_view(self):
        response = self.client.get(
            '/api/v1/releases/', HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        release_uri = data['objects'][0]['resource_uri']
        self.assertEquals(release_uri, '/api/v1/releases/11/')

        response = self.client.get(
            release_uri, HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(data['pub_date'], '2012-10-12')
        self.assertEquals(len(data['images']), 1)


class SubscriptionsResourceTestCase(TestCase):
    fixtures = ['comics.json']

    def setUp(self):
        self.user = create_user()
        create_subscriptions(self.user)
        self.client = Client()

    def test_requires_authentication(self):
        response = self.client.get('/api/v1/subscriptions/')

        self.assertEquals(response.status_code, 401)

    def test_authentication_with_secret_key_in_header(self):
        response = self.client.get(
            '/api/v1/subscriptions/', HTTP_AUTHORIZATION='Key s3cretk3y')

        self.assertEquals(response.status_code, 200)

    def test_list_subscriptions(self):
        subscription = Subscription.objects.all()[0]

        response = self.client.get(
            '/api/v1/subscriptions/', HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 2)

        sub = data['objects'][0]
        self.assertEquals(
            sub['resource_uri'],
            '/api/v1/subscriptions/%d/' % subscription.pk)
        self.assertEquals(
            sub['comic'],
            '/api/v1/comics/%d/' % subscription.comic.pk)

    def test_comic_filter(self):
        subscription = Subscription.objects.get(comic__slug='xkcd')

        response = self.client.get(
            '/api/v1/subscriptions/',
            {'comic__slug': 'xkcd'},
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 1)

        sub = data['objects'][0]
        self.assertEquals(
            sub['resource_uri'],
            '/api/v1/subscriptions/%d/' % subscription.pk)
        self.assertEquals(sub['comic'], '/api/v1/comics/9/')

    def test_details_view(self):
        subscription = Subscription.objects.all()[0]

        response = self.client.get(
            '/api/v1/subscriptions/', HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        sub = data['objects'][0]
        self.assertEquals(
            sub['resource_uri'],
            '/api/v1/subscriptions/%d/' % subscription.pk)

        response = self.client.get(
            sub['resource_uri'], HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(
            data['comic'], '/api/v1/comics/%d/' % subscription.comic.pk)

    def test_subscribe_to_comic(self):
        comic = Comic.objects.get(slug='bunny')

        data = json.dumps({'comic': '/api/v1/comics/%d/' % comic.pk})
        response = self.client.post(
            '/api/v1/subscriptions/',
            data=data, content_type='application/json',
            HTTP_AUTHORIZATION='Key s3cretk3y')

        self.assertEquals(response.status_code, 201)

        subscription = Subscription.objects.get(
            userprofile__user=self.user, comic=comic)
        self.assertEquals(
            response['Location'],
            '/api/v1/subscriptions/%d/' % subscription.pk)

        self.assertEquals(response.content, '')

    def test_unsubscribe_from_comic(self):
        sub = Subscription.objects.get(comic__slug='xkcd')

        self.assertEquals(
            2,
            Subscription.objects.filter(userprofile__user=self.user).count())

        response = self.client.delete(
            '/api/v1/subscriptions/%d/' % sub.pk,
            HTTP_AUTHORIZATION='Key s3cretk3y')

        self.assertEquals(response.status_code, 204)
        self.assertEquals(response.content, '')

        self.assertEquals(
            1,
            Subscription.objects.filter(userprofile__user=self.user).count())

    def test_bulk_update(self):
        # XXX: "PATCH /api/v1/subscriptions/" isn't tested as Django's test
        # client doesn't support the PATCH method yet. See
        # https://code.djangoproject.com/ticket/17797 to check if PATCH support
        # has been added yet.
        pass
