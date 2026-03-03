"""Sets QT_QPA_PLATFORM=offscreen so Qt-based tests work headlessly"""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
