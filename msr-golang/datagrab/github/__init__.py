from .commit import (
    grab_commits,
)

from .common import (
    load_access_token,
    load_repo_info,
)

from .repository import (
    collect_data,
)

from .gomod import (
    load_gomod,
    persist_gomod,
    persist_progress,
    load_mod_info,
    load_latest_ver,
    grab_gomod,
    grab_latest_version,
)

__version__ = "1.0.0"

__title__ = "MSR Data Grabber"
__description__ = "Golang dependency Research Data Grabber in Python"
__url__ = "https://github.com/schnell18"
__uri__ = __url__
__doc__ = f"{__description__} <{__uri__}>"

__author__ = "Justin Zhang"
__email__ = "schnell18@gmail.com"

__license__ = "MIT"
__copyright__ = "Copyright 2015-2023 Justin Zhang"


__all__ = [
    "load_access_token",
    "load_gomod",
    "persist_gomod",
    "persist_progress",
    "load_mod_info",
    "load_latest_ver",
    "grab_gomod",
    "grab_latest_version",
    "collect_data",
    "load_repo_info",
    "grab_commits",
]
