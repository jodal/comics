import base64
import json

from django.contrib.auth.models import User
from django.test.client import Client
from django.test import TestCase

from comics.accounts.models import Subscription
from comics.core.models import Comic


def create_user():
    user = User.objects.create_user('alice', 'alice@example.com', 'secret')
    user.comics_profile.secret_key = 's3cretk3y'
    user.comics_profile.save()
    return user


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
        self.assertEquals(data['releases']['list_endpoint'],
            '/api/v1/releases/')
        self.assertEquals(data['subscriptions']['list_endpoint'],
            '/api/v1/subscriptions/')

    def test_resource_can_return_xml(self):
        response = self.client.get('/api/v1/', HTTP_ACCEPT='application/xml')

        self.assertIn("<?xml version='1.0' encoding='utf-8'?>",
            response.content)

    def test_resource_can_return_jsonp(self):
        response = self.client.get('/api/v1/', {'format': 'jsonp'})

        self.assertIn('callback(', response.content)

    def test_resource_can_return_jsonp_with_custom_callback_name(self):
        response = self.client.get('/api/v1/', {'format': 'jsonp', 'callback': 'foo'})

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
        response = self.client.get('/api/v1/users/',
                HTTP_AUTHORIZATION='Basic %s' %
                base64.encodestring('alice:secret'))

        self.assertEquals(response.status_code, 200)

    def test_get_users_with_secret_key_in_header(self):
        response = self.client.get('/api/v1/users/',
            HTTP_AUTHORIZATION='Key s3cretk3y')

        self.assertEquals(response.status_code, 200)

    def test_get_users_with_secret_key_in_url(self):
        response = self.client.get('/api/v1/users/',
            {'key': 's3cretk3y'})

        self.assertEquals(response.status_code, 200)

    def test_response_returns_a_single_user_object(self):
        response = self.client.get('/api/v1/users/',
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 1)

    def test_response_includes_the_secret_key(self):
        response = self.client.get('/api/v1/users/',
            HTTP_AUTHORIZATION='Key s3cretk3y')

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
        response = self.client.get('/api/v1/comics/',
            HTTP_AUTHORIZATION='Key s3cretk3y')

        self.assertEquals(response.status_code, 200)

    def test_lists_comics(self):
        response = self.client.get('/api/v1/comics/',
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 10)
        self.assertEquals(data['objects'][0]['slug'], 'abstrusegoose')

    def test_slug_filter(self):
        response = self.client.get('/api/v1/comics/',
            {'slug': 'xkcd'},
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 1)
        self.assertEquals(data['objects'][0]['slug'], 'xkcd')

    def test_subscribed_filter(self):
        Subscription.objects.create(userprofile=self.user.comics_profile,
            comic=Comic.objects.get(slug='xkcd'))

        response = self.client.get('/api/v1/comics/',
            {'subscribed': 'true'},
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 1)
        self.assertEquals(data['objects'][0]['slug'], 'xkcd')

    def test_unsubscribed_filter(self):
        Subscription.objects.create(userprofile=self.user.comics_profile,
            comic=Comic.objects.get(slug='xkcd'))

        response = self.client.get('/api/v1/comics/',
            {'subscribed': 'false'},
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 9)
        self.assertEquals(data['objects'][0]['slug'], 'abstrusegoose')

    def test_details_view(self):
        response = self.client.get('/api/v1/comics/',
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        comic_uri = data['objects'][0]['resource_uri']
        self.assertEquals(comic_uri, '/api/v1/comics/1/')

        response = self.client.get(comic_uri,
            HTTP_AUTHORIZATION='Key s3cretk3y')

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
        response = self.client.get('/api/v1/images/',
            HTTP_AUTHORIZATION='Key s3cretk3y')

        self.assertEquals(response.status_code, 200)

    def test_lists_images(self):
        response = self.client.get('/api/v1/images/',
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 12)
        self.assertEquals(data['objects'][0]['height'], 1132)
        self.assertEquals(data['objects'][1]['title'],
            "Geek&Poke About The Good Ol' Days In Computers")

    def test_height_filter(self):
        response = self.client.get('/api/v1/images/',
            {'height__gt': 1100},
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 2)
        self.assertEquals(data['objects'][0]['height'], 1132)
        self.assertEquals(data['objects'][1]['height'], 1132)

    def test_details_view(self):
        response = self.client.get('/api/v1/images/',
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        image_uri = data['objects'][1]['resource_uri']
        self.assertEquals(image_uri, '/api/v1/images/2/')

        response = self.client.get(image_uri,
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(data['title'],
            "Geek&Poke About The Good Ol' Days In Computers")


class ReleasesResourceTestCase(TestCase):
    fixtures = ['comics.json']

    def setUp(self):
        self.user = create_user()
        self.client = Client()

    def test_requires_authentication(self):
        response = self.client.get('/api/v1/releases/')

        self.assertEquals(response.status_code, 401)

    def test_authentication_with_secret_key_in_header(self):
        response = self.client.get('/api/v1/releases/',
            HTTP_AUTHORIZATION='Key s3cretk3y')

        self.assertEquals(response.status_code, 200)

    def test_list_releases(self):
        response = self.client.get('/api/v1/releases/',
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 11)

        release = data['objects'][0]
        self.assertEquals(release['comic'], '/api/v1/comics/9/')
        self.assertEquals(release['pub_date'], '2012-10-12')
        self.assertEquals(release['resource_uri'],
            '/api/v1/releases/11/')
        self.assertEquals(len(release['images']), 1)

        image = release['images'][0]
        self.assertEquals(image['title'], 'Blurring the Line')
        self.assertEquals(image['text'], 'People into masturbatory ' +
            'navel-gazing have a lot to learn about masturbation.')
        self.assertEquals(image['height'], 235)
        self.assertEquals(image['width'], 740)
        self.assertEquals(image['checksum'],
            '76a1407a2730b000d51ccf764c689c8930fdd3580e01f62f70cbe73d8be17e9c')

    def test_subscribed_filter(self):
        Subscription.objects.create(userprofile=self.user.comics_profile,
            comic=Comic.objects.get(slug='xkcd'))

        response = self.client.get('/api/v1/releases/',
            {'subscribed': 'true'},
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 4)

    def test_comic_filter(self):
        response = self.client.get('/api/v1/releases/',
            {'comic__slug': 'geekandpoke'},
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 2)

        release = data['objects'][0]
        self.assertEquals(release['comic'], '/api/v1/comics/4/')

    def test_pub_date_filter(self):
        response = self.client.get('/api/v1/releases/',
            {'pub_date__year': 2012, 'pub_date__month': 10},
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 11)

        response = self.client.get('/api/v1/releases/',
            {'pub_date__year': 2012, 'pub_date__month': 9},
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(len(data['objects']), 0)

    def test_unknown_filter_fails(self):
        response = self.client.get('/api/v1/releases/',
            {'pub_date__foo': 'bar'},
            HTTP_AUTHORIZATION='Key s3cretk3y')

        self.assertEquals(response.status_code, 400)

    def test_details_view(self):
        response = self.client.get('/api/v1/releases/',
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        release_uri = data['objects'][0]['resource_uri']
        self.assertEquals(release_uri, '/api/v1/releases/11/')

        response = self.client.get(release_uri,
            HTTP_AUTHORIZATION='Key s3cretk3y')

        data = json.loads(response.content)
        self.assertEquals(data['pub_date'], '2012-10-12')
        self.assertEquals(len(data['images']), 1)


class SubscriptionsResourceTestCase(TestCase):
    def setUp(self):
        create_user()
        self.client = Client()

    def test_requires_authentication(self):
        response = self.client.get('/api/v1/subscriptions/')

        self.assertEquals(response.status_code, 401)

    def test_authentication_with_secret_key_in_header(self):
        response = self.client.get('/api/v1/subscriptions/',
            HTTP_AUTHORIZATION='Key s3cretk3y')

        self.assertEquals(response.status_code, 200)

    # TODO
