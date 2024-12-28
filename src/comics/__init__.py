import logging

# Install a default log handler so that we don't get errors about missing log
# handlers when running tests.
logging.getLogger("comics").addHandler(logging.NullHandler())
