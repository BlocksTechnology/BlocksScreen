from .components import load_components

# NOTE: dbus_service (which imports sdbus) is intentionally NOT imported here so
# that the CLI (status/update/recover) runs on an interpreter without sdbus. The
# daemon imports updater.dbus_service explicitly.
from .executor import (
    apt_update,
    apt_upgrade,
    check_apt_status,
    check_git_status,
    git_commits_behind,
    git_describe,
    git_fetch,
    git_get_hash,
    git_is_dirty,
    git_prune_extra_remotes,
    git_pull,
    git_remote_url,
    git_reset_to_hash,
    restart_service,
)
from .models import ComponentConfig, ComponentStatus
from .service import LoggingCallback, ProgressCallback, UpdateService

__all__ = [
    # Components
    "ComponentConfig",
    "ComponentStatus",
    "load_components",
    # Executor
    "apt_update",
    "apt_upgrade",
    "check_apt_status",
    "check_git_status",
    "git_commits_behind",
    "git_describe",
    "git_fetch",
    "git_get_hash",
    "git_is_dirty",
    "git_prune_extra_remotes",
    "git_pull",
    "git_remote_url",
    "git_reset_to_hash",
    "restart_service",
    # Service
    "LoggingCallback",
    "ProgressCallback",
    "UpdateService",
]
