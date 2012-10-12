import logging

# Install a default log handler so that we don't get errors about missing log
# handlers when running tests.
#
# logging.NullHandler is new in Python 2.7, so we do this conditionally.
if hasattr(logging, 'NullHandler'):
    logging.getLogger().addHandler(logging.NullHandler())
