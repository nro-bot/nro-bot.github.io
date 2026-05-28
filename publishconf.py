# Production settings — used when building for deployment (e.g. the GitHub
# Actions workflow and `make publish`). Imports everything from pelicanconf.py
# and overrides the values that differ in production.
import os
import sys

sys.path.append(os.curdir)
from pelicanconf import *  # noqa: F401,F403

# Absolute URL of the live site. Assets and internal links are built against
# this when publishing.
SITEURL = "https://nrobot.dev"
RELATIVE_URLS = False

DELETE_OUTPUT_DIRECTORY = True

# Feeds (left off for the portfolio; enable if you add a blog section)
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
