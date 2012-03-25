import os

PROJECT_DIR = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..'))

SECRET_KEY = ''

DATABASES = {
    'default': {
        'NAME': os.path.abspath(os.path.join(PROJECT_DIR, '..', 'db.sqlite3')),
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

TIME_ZONE = 'Europe/Oslo'
LANGUAGE_CODE = 'en-us'

USE_I18N = False
USE_L10N = True
USE_TZ = True

SITE_ID = 1

MEDIA_ROOT = os.path.abspath(os.path.join(PROJECT_DIR, '..', 'media'))
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.abspath(os.path.join(PROJECT_DIR, '..', 'static'))
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
    'comics.sets.context_processors.user_set',
)

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
    'comics.core.middleware.MinifyHTMLMiddleware',
    'comics.sets.middleware.SetMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.webdesign',
    'bootstrapform',
    'compressor',
    'registration',
    'south',
    'comics.aggregator',
    'comics.core',
    'comics.accounts',
    'comics.feedback',
    'comics.meta',
    'comics.sets',
    'comics.utils',
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

DATE_FORMAT = 'D j M Y'
TIME_FORMAT = 'H:i'

SESSION_COOKIE_AGE = 86400 * 365

WSGI_APPLICATION = 'comics.wsgi.application'


### django_compressor settings

# Explicitly use HtmlParser to avoid depending on BeautifulSoup through the use
# of LxmlParser
COMPRESS_PARSER = 'compressor.parser.HtmlParser'

# Turn on CSS compression. JS compression is on by default if jsmin is installed
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

ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_REDIRECT_URL = '/'
REGISTRATION_BACKEND = 'comics.accounts.backends.RegistrationBackend'


### comics settings

# Location of the comic images
COMICS_MEDIA_ROOT = os.path.join(MEDIA_ROOT, 'c')
COMICS_MEDIA_URL = MEDIA_URL + 'c/'

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
COMICS_LOG_FILENAME = os.path.abspath(
    os.path.join(PROJECT_DIR, '..', 'comics.log'))

# Time zone used for comic crawlers without a specified time zone
# UTC=0, CET=1, EST=-5, PST=-8
COMICS_DEFAULT_TIME_ZONE = 1

# Google Analytics tracking code
COMICS_GOOGLE_ANALYTICS_CODE = None
