import os

PROJECT_DIR = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..'))

SECRET_KEY = ''

#: Database settings. You will want to change this for production. See the
#: Django docs for details.
DATABASES = {
    'default': {
        'NAME': os.path.abspath(os.path.join(PROJECT_DIR, '..', 'db.sqlite3')),
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

#: Time zone of the server. Used by Django's time zone support
#: handling in comics
TIME_ZONE = 'Europe/Oslo'

LANGUAGE_CODE = 'en-us'

USE_I18N = False
USE_L10N = True
USE_TZ = True

#: Path on disk to where downloaded media will be stored and served from
MEDIA_ROOT = os.path.abspath(os.path.join(PROJECT_DIR, '..', 'media'))

#: URL to where downloaded media will be stored and served from
MEDIA_URL = '/media/'

#: Path on disk to where static files will be served from
STATIC_ROOT = os.path.abspath(os.path.join(PROJECT_DIR, '..', 'static'))

#: URL to where static files will be served from
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'comics.core.context_processors.site_settings',
    'comics.core.context_processors.all_comics',
)

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.app_directories.Loader',
    )),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'comics.core.middleware.MinifyHTMLMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'bootstrapform',
    'compressor',
    'invitation',
    'registration',
    'south',
    'comics.core',
    'comics.accounts',
    'comics.aggregator',
    'comics.browser',
    'comics.help',
    'comics.status',
)

ROOT_URLCONF = 'comics.urls'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
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

DATE_FORMAT = 'l j F Y'
TIME_FORMAT = 'H:i'

#: Time the user session cookies will be valid. 1 year by default.
SESSION_COOKIE_AGE = 86400 * 365

WSGI_APPLICATION = 'comics.wsgi.application'


### django_compressor settings

# Explicitly use HtmlParser to avoid depending on BeautifulSoup through the use
# of LxmlParser
COMPRESS_PARSER = 'compressor.parser.HtmlParser'

# Turn on CSS compression. JS compression is on by default if jsmin is
# installed
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]

# Turn on HTML compression through custom middleware
COMPRESS_HTML = True


### django.contrib.auth settings

LOGIN_URL = '/account/login/'
AUTH_PROFILE_MODULE = 'accounts.UserProfile'
AUTHENTICATION_BACKENDS = (
    'comics.accounts.backends.AuthBackend',
    'django.contrib.auth.backends.ModelBackend'
)


### django-registration settings

#: Number of days an the account activation link will work
ACCOUNT_ACTIVATION_DAYS = 7

LOGIN_REDIRECT_URL = '/'
REGISTRATION_BACKEND = 'comics.accounts.backends.RegistrationBackend'


### django-invitation settings

#: Turn invitations off by default, leaving the site open for user registrations
INVITE_MODE = False

#: Number of days an invitation will be valid
ACCOUNT_INVITATION_DAYS = 7

#: Number of invitations each existing user can send
INVITATIONS_PER_USER = 10


### comics settings

#: Name of the site. Used in page header, page title, feed titles, etc.
COMICS_SITE_TITLE = 'example.com'

#: Maximum number of releases to show on one page
COMICS_MAX_RELEASES_PER_PAGE = 50

#: Maximum number of days to show in a feed
COMICS_MAX_DAYS_IN_FEED = 30

#: SHA256 of blacklisted images
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
    # GoComics
    '60478320f08212249aefaa3ac647fa182dc7f0d7b70e5691c5f95f9859319bdf',
    # Least I Could Do
    '38eca900236617b2c38768c5e5fa410544fea7a3b79cc1e9bd45043623124dbf',
)

#: Comics log file path on disk
COMICS_LOG_FILENAME = os.path.abspath(
    os.path.join(PROJECT_DIR, '..', 'comics.log'))

#: Time zone of the server's clock. Used for comic crawlers without a specified
#: time zone, and to calculate the offset of other crawlers.
#:
#: Examples: UTC=0, CET=1, EST=-5, PST=-8.
#:
#: This should be replaced by Django 1.4's time zone support.
COMICS_DEFAULT_TIME_ZONE = 1

#: Google Analytics tracking code. Tracking code will be included on all pages
#: if this is set.
COMICS_GOOGLE_ANALYTICS_CODE = None

#: Number of seconds browsers at the latest view of "My comics" should wait before
#: they check for new releases again
COMICS_BROWSER_REFRESH_INTERVAL = 60

#: Number of days a new comic on the site is labeled as new
COMICS_NUM_DAYS_COMIC_IS_NEW = 7
