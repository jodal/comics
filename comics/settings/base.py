# Django settings for comics project.

import os
import django

PROJECT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../')
DJANGO_DIR = os.path.dirname(os.path.abspath(django.__file__))

SECRET_KEY = 'This key should really be overriden in comics/settings/local.py'

DATABASES = {
    'default': {
        'NAME': os.path.join(PROJECT_DIR, '../db.sqlite3'),
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

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

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

SITE_ID = 1

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.abspath(os.path.join(PROJECT_DIR, '../media/')) + '/'

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.abspath(os.path.join(PROJECT_DIR, '../static/'))

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'comics.sets.middleware.SetMiddleware',
)

ROOT_URLCONF = 'comics.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'comics.core.context_processors.site_settings',
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
    'django.contrib.staticfiles',
    'django.contrib.webdesign',
    'compressor',
    'south',
    'comics.aggregator',
    'comics.core',
    'comics.feedback',
    'comics.meta',
    'comics.sets',
    'comics.utils',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'TIMEOUT': 300,
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
        },
    }
}
CACHE_MIDDLEWARE_SECONDS = 300
CACHE_MIDDLEWARE_KEY_PREFIX = 'comics'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

# Formats
DATE_FORMAT = 'D j M Y'
TIME_FORMAT = 'H:i'

# Haystack settings, only apply if comics.search and haystack are used
HAYSTACK_SITECONF = 'comics.search.indexes'
HAYSTACK_SEARCH_ENGINE = 'solr'
HAYSTACK_SOLR_URL = 'http://127.0.0.1:8983/solr'

# django_compressor settings
# Explicitly use HtmlParser to avoid depending on BeautifulSoup through the use
# of LxmlParser
COMPRESS_PARSER = 'compressor.parser.HtmlParser'

### Additional non-Django settings used by comics

# Name of the site, used in e.g. feeds
COMICS_SITE_TITLE = 'Daily Comics'
COMICS_SITE_TAGLINE = 'your personal comics aggregator'

# Location of the comic images
COMICS_MEDIA_ROOT = '%sc/' % MEDIA_ROOT
COMICS_MEDIA_URL = '%sc/' % MEDIA_URL

# Number of comics to show in the top list
COMICS_MAX_IN_TOP_LIST = 10

# Maximum number of days to show in one page
COMICS_MAX_DAYS_IN_PAGE = 31

# Maximum number of days to show in a feed
COMICS_MAX_DAYS_IN_FEED = 30

# SHA256 of blacklisted images
COMICS_IMAGE_BLACKLIST = (
    # Empty file
    'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    # Billy
    'f8021551b772384d1f4309e0ee15c94cea9ec1e61ba0a7aade8036e40e3179fe',
    # Bizarro
    'dd040144f802bab9b96892cc2e1be26b226e7b43b275aa49dbcc9c4a254d6782',
    # Dagbladet.no
    '61c66a1c84408df5b855004dd799d5e59f4af99f4c6fe8bf4aabf8963cab7cb5',
    # Cyanide and Happiness
    '01237a79e2a283718059e4a180a01e8ffa9f9b36af7e0cad5650dd1a08665971',
    '181e7d11ebd3224a910d9eba2995349da5d483f3ae9643a2efe4f7dd3d9f668d',
    '6dec8be9787fc8b103746886033ccad7348bc4eec44c12994ba83596f3cbcd32',
    'f56248bf5b94b324d495c3967e568337b6b15249d4dfe7f9d8afdca4cb54cd29',
    '0a929bfebf333a16226e0734bbaefe3b85f9c615ff8fb7a777954793788b6e34',
    # Dilbert (bt.no)
    'cde5b71cfb91c05d0cd19f35e325fc1cc9f529dfbce5c6e2583a3aa73d240638',
    # Least I Could Do
    '38eca900236617b2c38768c5e5fa410544fea7a3b79cc1e9bd45043623124dbf',
)

# Comics log file
COMICS_LOG_FILENAME = os.path.join(PROJECT_DIR, '../comics.log')

# Time zone used for comic crawlers without a specified time zone
# UTC=0, CET=1, EST=-5, PST=-8
COMICS_DEFAULT_TIME_ZONE = 1

# Google Analytics tracking code
COMICS_GOOGLE_ANALYTICS_CODE = None
