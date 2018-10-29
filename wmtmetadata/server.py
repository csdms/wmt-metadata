"""Get information about the WMT server in which metadata are installed."""

import os
import sys


prefix = os.path.dirname(sys.prefix)

components_dir = os.path.join(prefix, 'db', 'components')
hosts_dir = os.path.join(prefix, 'db', 'hosts')
