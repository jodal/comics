from pathlib import Path
from urllib.parse import urlsplit

import dj_database_url
import sentry_sdk
from django.core.management.utils import get_random_secret_key
from sentry_sdk.integrations.django import DjangoIntegration
from typenv import Env

# Paths
#
# During development, we keep generated files in a "run" directory in the
# repo root.
RUN_DIR = Path(__file__).parents[2] / "run"


# Environment variables
# https://github.com/hukkin/typenv
#
env = Env()
env.read_env(".env")


# Debug mode
# Keep off in production!
#
DEBUG = env.bool(
    "DJANGO_DEBUG",
    default=False,
)
#
INTERNAL_IPS = [
    "127.0.0.1"  # Required by django-debug-toolbar
]


# Sentry crash reporting
#
# To enable Sentry crash reporting, set the SENTRY_DSN environment variable.
SENTRY_DSN = env.str("SENTRY_DSN", default=None)
SENTRY_TRACES_SAMPLE_RATE = env.float("SENTRY_TRACES_SAMPLE_RATE", default=0)
sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[DjangoIntegration()],
    traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
    send_default_pii=True,
)


# Security - Django's secret key
#
SECRET_KEY = env.str(
    "DJANGO_SECRET_KEY",
    default=get_random_secret_key(),
)


# Security - Allowed hosts
#
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["*"])


# Security - Cross-Site Request Forgery (CSRF)
#
CSRF_TRUSTED_ORIGINS = env.list(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    default=["http://localhost:8000"],
)


# Security - Session
#
# Time the user session cookies will be valid. Default: 1 year
SESSION_COOKIE_AGE = 60 * 60 * 24 * 365


# Application definition
#
ROOT_URLCONF = "comics.urls"
WSGI_APPLICATION = "comics.wsgi.application"


# Installed apps
#
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
]
LOCAL_APPS = [
    "comics.core",
    "comics.accounts",
    "comics.aggregator",
    "comics.api",
    "comics.browser",
    "comics.help",
    "comics.status",
]
THIRD_PARTY_APPS = [
    "allauth",
    "allauth.account",
    "invitations",  # After allauth
    "bootstrapform",
    "compressor",
    "tastypie",
]
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS


# Middleware
#
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


# Templates
#
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
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
        },
    },
]


# Cache
#
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "TIMEOUT": 300,
        "OPTIONS": {"MAX_ENTRIES": 1000},
    }
}
if cache_url := env.str("CACHE_URL", default=None):
    parts = urlsplit(cache_url)
    if parts.scheme == "memcache":
        CACHES["default"] = {
            "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
            "LOCATION": parts.netloc,
        }
        SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
#
CACHE_MIDDLEWARE_SECONDS = 300
CACHE_MIDDLEWARE_KEY_PREFIX = "comics"
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True


# Database
#
# SQLite is used by default by tests and development. In production, you should
# set the DATABASE_URL environment variable to use a PostgreSQL database.
SQLITE_FILE = str(RUN_DIR / "db.sqlite3")
SQLITE_URL = f"sqlite:///{SQLITE_FILE}"
#
DATABASES = {
    "default": dj_database_url.parse(
        env.str(
            "DATABASE_URL",
            default=SQLITE_URL,
        ),
    ),
}
#
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Email
#
DEFAULT_FROM_EMAIL = env.str(
    "DJANGO_DEFAULT_FROM_EMAIL",
    default="webmaster@example.com",
)
#
# Email backend to use.
# Default sends emails to console output, which is useful for development.
EMAIL_BACKEND = env.str(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.console.EmailBackend",
)
#
# Send email using Anymail via SendGrid if SENDGRID_API_KEY is set.
if sendgrid_api_key := env.str("SENDGRID_API_KEY", default=None):
    EMAIL_BACKEND = "anymail.backends.sendgrid.EmailBackend"
    ANYMAIL = {
        "SENDGRID_API_KEY": sendgrid_api_key,
    }


# Auth - django.contrib.auth
#
AUTH_PROFILE_MODULE = "accounts.UserProfile"
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "account_login"


# Auth - django-allauth
#
SITE_ID = 1
ACCOUNT_ADAPTER = "invitations.models.InvitationsAdapter"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[%s] " % (
    env.str("COMICS_SITE_TITLE", default="example.com")
)
ACCOUNT_USERNAME_REQUIRED = False


# Auth - django-invitations
#
INVITATIONS_ADAPTER = ACCOUNT_ADAPTER
INVITATIONS_INVITATION_ONLY = env.bool("COMICS_INVITE_MODE", default=False)


# Internationalization
#
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = False
USE_TZ = True
#
DATE_FORMAT = "l j F Y"
TIME_FORMAT = "H:i"


# Static files (CSS, JavaScript, etc.)
#
# Path on disk to where static files will be collected to and served from.
STATIC_ROOT = env.str(
    "DJANGO_STATIC_ROOT",
    default=str(RUN_DIR / "static"),
)
Path(STATIC_ROOT).mkdir(parents=True, exist_ok=True)
#
# URL to where static files will be served from.
STATIC_URL = env.str(
    "DJANGO_STATIC_URL",
    default="/static/",
)
#
STATICFILES_DIRS = [
    str(Path(__file__).parent / "static"),
]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]


# Static files - django-compressor
#
# Explicitly use HtmlParser to avoid depending on BeautifulSoup through the use
# of LxmlParser
COMPRESS_PARSER = "compressor.parser.HtmlParser"
#
# Turn on CSS and JS compression
COMPRESS_FILTERS = {
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.rCSSMinFilter",
    ],
    "js": [
        "compressor.filters.jsmin.rJSMinFilter",
    ],
}


# Media files (comic images, etc.)
#
# Path on disk to where downloaded media will be stored and served from.
MEDIA_ROOT = env.str(
    "DJANGO_MEDIA_ROOT",
    default=str(RUN_DIR / "media"),
)
Path(MEDIA_ROOT).mkdir(parents=True, exist_ok=True)
#
# URL to where downloaded media will be stored and served from.
MEDIA_URL = env.str(
    "DJANGO_MEDIA_URL",
    default="/media/",
)


# API - django-tastypie
#
TASTYPIE_DEFAULT_FORMATS = ["json", "jsonp", "xml", "yaml", "plist"]


# Tests
#
TEST_RUNNER = "django.test.runner.DiscoverRunner"


# Development - django-debug-toolbar
#
try:
    import debug_toolbar  # noqa: F401
except ImportError:
    pass
else:
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INSTALLED_APPS += ["debug_toolbar"]


# Development - django-extensions
#
try:
    import django_extensions  # noqa: F401
except ImportError:
    pass
else:
    INSTALLED_APPS += ["django_extensions"]


# Comics
#
# Name of the site. Used in page header, page title, feed titles, etc.
COMICS_SITE_TITLE = env.str(
    "COMICS_SITE_TITLE",
    default="example.com",
)
#
# Maximum number of releases to show on one page
COMICS_MAX_RELEASES_PER_PAGE = env.int(
    "COMICS_MAX_RELEASES_PER_PAGE",
    default=50,
)
#
# Maximum number of days to show in a feed
COMICS_MAX_DAYS_IN_FEED = env.int(
    "COMICS_MAX_DAYS_IN_FEED",
    default=30,
)
#
# SHA256 of blacklisted images
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
    # Dilbert from bt.no
    "cde5b71cfb91c05d0cd19f35e325fc1cc9f529dfbce5c6e2583a3aa73d240638",
    # GoComics
    "60478320f08212249aefaa3ac647fa182dc7f0d7b70e5691c5f95f9859319bdf",
    # Least I Could Do
    "38eca900236617b2c38768c5e5fa410544fea7a3b79cc1e9bd45043623124dbf",
    # tu.no
    "e90e3718487c99190426b3b38639670d4a3ee39c1e7319b9b781740b0c7a53bf",
]
#
# Comics log file path on disk
COMICS_LOG_FILENAME = env.str(
    "COMICS_LOG_FILENAME",
    default=str(RUN_DIR / "comics.log"),
)
#
# Google Analytics
# Tracking code will be included on all pages if this is set.
COMICS_GOOGLE_ANALYTICS_CODE = env.str(
    "COMICS_GOOGLE_ANALYTICS_CODE",
    default="",
)
#
# Number of seconds browsers at the latest view of "My comics" should wait
# before they check for new releases again
COMICS_BROWSER_REFRESH_INTERVAL = env.int(
    "COMICS_BROWSER_REFRESH_INTERVAL",
    default=60,
)
#
# Number of days a new comic on the site is labeled as new
COMICS_NUM_DAYS_COMIC_IS_NEW = env.int(
    "COMICS_NUM_DAYS_COMIC_IS_NEW",
    default=7,
)
