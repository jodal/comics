import logging
import warnings

from django.utils.deprecation import RemovedInDjango40Warning

# Install a default log handler so that we don't get errors about missing log
# handlers when running tests.
logging.getLogger("comics").addHandler(logging.NullHandler())

# Filter warnings from dependencies with known deprecation warnings to that we
# can spot any warnings from our own code.
warnings.filterwarnings(
    action="ignore",
    category=RemovedInDjango40Warning,
    module="invitations",
)
warnings.filterwarnings(
    action="ignore",
    category=RemovedInDjango40Warning,
    module="tastypie",
)
