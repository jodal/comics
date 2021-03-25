import os

import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

root = environ.Path(os.path.dirname(os.path.dirname(__file__)))

env = environ.Env()
env.read_env(root(".env"))


#: The Django secret key
SECRET_KEY = env.str("DJANGO_SECRET_KEY")

#: Debug mode. Keep off in production.
DEBUG = env.bool("DJANGO_DEBUG", default=False)

#: Site admins
ADMINS = []
if "DJANGO_ADMIN" in env:
    ADMINS.append(("Site admin", env.str("DJANGO_ADMIN")))

#: Default from email
DEFAULT_FROM_EMAIL = env.str(
    "DJANGO_DEFAULT_FROM_EMAIL", default="webmaster@example.com"
)

SQLITE_FILE = root("db.sqlite3")
SQLITE_URL = "sqlite:///" + os.path.abspath(SQLITE_FILE)

#: Database settings. You will want to change this for production. See the
#: Django docs for details.
DATABASES = {
    "default": env.db("DATABASE_URL", default=SQLITE_URL),
}

#: Default time zone to use when displaying datetimes to users
TIME_ZONE = "UTC"

LANGUAGE_CODE = "en-us"

USE_I18N = False
USE_L10N = False
USE_TZ = True

#: Path on disk to where downloaded media will be stored and served from
MEDIA_ROOT = env.str("DJANGO_MEDIA_ROOT", default=root("media"))

#: URL to where downloaded media will be stored and served from
MEDIA_URL = env.str("DJANGO_MEDIA_URL", default="/media/")

#: Path on disk to where static files will be served from
STATIC_ROOT = env.str("DJANGO_STATIC_ROOT", default=root("static"))

#: URL to where static files will be served from
STATIC_URL = env.str("DJANGO_STATIC_URL", default="/static/")

STATICFILES_DIRS = [
    root("comics/static"),
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            # insert your TEMPLATE_DIRS here
        ],
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.contrib.messages.context_processors.messages",
                "comics.core.context_processors.site_settings",
                "comics.core.context_processors.all_comics",
            ],
            "loaders": [
                (
                    "django.template.loaders.cached.Loader",
                    ["django.template.loaders.app_directories.Loader"],
                ),
            ],
        },
    },
]

if DEBUG:
    TEMPLATES[0]["OPTIONS"]["loaders"] = [
        "django.template.loaders.app_directories.Loader",
    ]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.http.ConditionalGetMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    # Our apps
    "comics.core",
    "comics.accounts",
    "comics.aggregator",
    "comics.api",
    "comics.browser",
    "comics.help",
    "comics.status",
    # Third party apps
    "allauth",
    "allauth.account",
    "invitations",  # After allauth
    "bootstrapform",
    "compressor",
    "tastypie",
]

ROOT_URLCONF = "comics.urls"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "handlers": {
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        }
    },
    "loggers": {
        "django.request": {
            "handlers": ["mail_admins"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "TIMEOUT": 300,
        "OPTIONS": {"MAX_ENTRIES": 1000},
    }
}
if "CACHE_URL" in env:
    CACHES["default"] = env.cache("CACHE_URL")
    SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

CACHE_MIDDLEWARE_SECONDS = 300
CACHE_MIDDLEWARE_KEY_PREFIX = "comics"
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True


DATE_FORMAT = "l j F Y"
TIME_FORMAT = "H:i"

#: Time the user session cookies will be valid. 1 year by default.
SESSION_COOKIE_AGE = 86400 * 365

TEST_RUNNER = "django.test.runner.DiscoverRunner"

WSGI_APPLICATION = "comics.wsgi.application"

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default="*")


# ### djang-debug-toolbar settings

try:
    import debug_toolbar  # noqa
except ImportError:
    pass
else:
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INSTALLED_APPS += ["debug_toolbar"]


# ### django-extensions settings

try:
    import django_extensions  # noqa
except ImportError:
    pass
else:
    INSTALLED_APPS += ["django_extensions"]


# ### django_compressor settings

# Explicitly use HtmlParser to avoid depending on BeautifulSoup through the use
# of LxmlParser
COMPRESS_PARSER = "compressor.parser.HtmlParser"

# Turn on CSS compression. JS compression is on by default if jsmin is
# installed
COMPRESS_CSS_FILTERS = [
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter",
]

# Turn on HTML compression through custom middleware
COMPRESS_HTML = True


# ### django.contrib.auth settings

LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "/"
AUTH_PROFILE_MODULE = "accounts.UserProfile"
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]


# ### django-allauth settings

SITE_ID = 1
ACCOUNT_ADAPTER = "invitations.models.InvitationsAdapter"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[%s] " % (
    env.str("COMICS_SITE_TITLE", default="example.com")
)
ACCOUNT_USERNAME_REQUIRED = False


# ### django-invitations settings

INVITATIONS_ADAPTER = ACCOUNT_ADAPTER
INVITATIONS_INVITATION_ONLY = env.bool("COMICS_INVITE_MODE", default=False)


# ### Tastypie settings

TASTYPIE_DEFAULT_FORMATS = ["json", "jsonp", "xml", "yaml", "plist"]


# ### Sentry settings

SENTRY_DSN = env.str("SENTRY_DSN", default=None)

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)


# ### comics settings

#: Name of the site. Used in page header, page title, feed titles, etc.
COMICS_SITE_TITLE = env.str("COMICS_SITE_TITLE", default="example.com")

#: Maximum number of releases to show on one page
COMICS_MAX_RELEASES_PER_PAGE = env.int("COMICS_MAX_RELEASES_PER_PAGE", default=50)

#: Maximum number of days to show in a feed
COMICS_MAX_DAYS_IN_FEED = env.int("COMICS_MAX_DAYS_IN_FEED", default=30)

#: SHA256 of blacklisted images
COMICS_IMAGE_BLACKLIST = [
    # Empty file
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    # Billy
    "f8021551b772384d1f4309e0ee15c94cea9ec1e61ba0a7aade8036e40e3179fe",
    # Bizarro
    "dd040144f802bab9b96892cc2e1be26b226e7b43b275aa49dbcc9c4a254d6782",
    # Dagbladet.no
    "61c66a1c84408df5b855004dd799d5e59f4af99f4c6fe8bf4aabf8963cab7cb5",
    # Cyanide and Happiness
    "01237a79e2a283718059e4a180a01e8ffa9f9b36af7e0cad5650dd1a08665971",
    "181e7d11ebd3224a910d9eba2995349da5d483f3ae9643a2efe4f7dd3d9f668d",
    "6dec8be9787fc8b103746886033ccad7348bc4eec44c12994ba83596f3cbcd32",
    "f56248bf5b94b324d495c3967e568337b6b15249d4dfe7f9d8afdca4cb54cd29",
    "0a929bfebf333a16226e0734bbaefe3b85f9c615ff8fb7a777954793788b6e34",
    # Dilbert (bt.no)
    "cde5b71cfb91c05d0cd19f35e325fc1cc9f529dfbce5c6e2583a3aa73d240638",
    # GoComics
    "60478320f08212249aefaa3ac647fa182dc7f0d7b70e5691c5f95f9859319bdf",
    # Least I Could Do
    "38eca900236617b2c38768c5e5fa410544fea7a3b79cc1e9bd45043623124dbf",
    # tu.no
    "e90e3718487c99190426b3b38639670d4a3ee39c1e7319b9b781740b0c7a53bf",
]

#: Comics log file path on disk
COMICS_LOG_FILENAME = env.str("COMICS_LOG_FILENAME", default=root("comics.log"))

#: Google Analytics tracking code. Tracking code will be included on all pages
#: if this is set.
COMICS_GOOGLE_ANALYTICS_CODE = env.str("COMICS_GOOGLE_ANALYTICS_CODE", default="")

#: Number of seconds browsers at the latest view of "My comics" should wait
#: before they check for new releases again
COMICS_BROWSER_REFRESH_INTERVAL = env.int("COMICS_BROWSER_REFRESH_INTERVAL", default=60)

#: Number of days a new comic on the site is labeled as new
COMICS_NUM_DAYS_COMIC_IS_NEW = env.int("COMICS_NUM_DAYS_COMIC_IS_NEW", default=7)
