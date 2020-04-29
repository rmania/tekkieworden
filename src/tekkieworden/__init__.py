import logging

from tekkieworden.config import config

VERSION_PATH = config.PROJECT_ROOT / 'VERSION'

# Configure logger for use in package
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

with open(VERSION_PATH, 'r') as version_file:
    __version__ = version_file.read().strip()