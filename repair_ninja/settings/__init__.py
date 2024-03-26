"""
Initials Django settings based on your environment mode.
"""

import os

from .base import *

MODE = os.environ.get('REPAIR_NINJA_MODE', 'PROD')

if MODE == 'PROD':
    from .prod import *
elif MODE == 'DEV':
    from .dev import *
