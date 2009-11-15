# Django settings for comics project.

import os
import django

PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')
DJANGO_DIR = os.path.dirname(os.path.abspath(django.__file__))

SECRET_KEY = 'This key should really be overriden in comics/settings/local.py'

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(PROJECT_DIR, '../db.sqlite3')

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'Europe/Oslo'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

SITE_ID = 1

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, '../media/')

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin/media/'
ADMIN_MEDIA_ROOT = os.path.join(DJANGO_DIR, 'contrib/admin/media/')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'comics.sets.middleware.SetMiddleware',
)

ROOT_URLCONF = 'comics.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'comics.core.context_processors.all_comics',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    'comics.core',
    'comics.crawler',
    'comics.feedback',
    'comics.sets',
    'comics.utils',
)

# Caching
CACHE_BACKEND = 'locmem:///'
CACHE_MIDDLEWARE_SECONDS = 300
CACHE_MIDDLEWARE_KEY_PREFIX = 'comics'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

# Formats
DATE_FORMAT = 'D j M Y'
TIME_FORMAT = 'H:i'


### Additional non-Django settings used by comics

# Name of the site, used in e.g. feeds
COMICS_SITE_TITLE = 'Daily Comics'

# Location of the comic strip images
COMICS_MEDIA_ROOT = '%sc/' % MEDIA_ROOT
COMICS_MEDIA_URL = '%sc/' % MEDIA_URL

# Number of comics to show in the top list
COMICS_MAX_IN_TOP_LIST = 10

# Maximum number of days to show in one page
COMICS_MAX_DAYS_IN_PAGE = 31

# Maximum number of days to show in a feed
COMICS_MAX_DAYS_IN_FEED = 30

# SHA256 of blacklisted comic strips
COMICS_STRIP_BLACKLIST = (
    # Dagbladet.no
    '61c66a1c84408df5b855004dd799d5e59f4af99f4c6fe8bf4aabf8963cab7cb5',
    # Cyanide and Happiness
    '6dec8be9787fc8b103746886033ccad7348bc4eec44c12994ba83596f3cbcd32',
    '181e7d11ebd3224a910d9eba2995349da5d483f3ae9643a2efe4f7dd3d9f668d',
    # Dilbert (bt.no)
    'cde5b71cfb91c05d0cd19f35e325fc1cc9f529dfbce5c6e2583a3aa73d240638',
    # Least I Could Do
    '38eca900236617b2c38768c5e5fa410544fea7a3b79cc1e9bd45043623124dbf',
)

# Comics log file
COMICS_LOG_FILENAME = os.path.join(PROJECT_DIR, '../comics.log')

# Python package containing the crawlers
COMICS_CRAWLER_PACKAGE = 'comics.crawler.crawlers'
