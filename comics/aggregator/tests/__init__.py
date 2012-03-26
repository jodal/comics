import logging
import os

from comics.aggregator.tests.command import *  # NOQA
from comics.aggregator.tests.crawler import *  # NOQA

logging.basicConfig(level=logging.CRITICAL, filename=os.devnull)
