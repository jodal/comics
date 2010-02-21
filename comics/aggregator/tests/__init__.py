import logging
import os

from comics.aggregator.tests.command import *
from comics.aggregator.tests.crawler import *

logging.basicConfig(level=logging.CRITICAL, filename=os.devnull)
