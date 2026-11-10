"""Updater package; dbus_service stays unimported so the CLI runs without sdbus."""

from .components import load_components

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
    "ComponentConfig",
    "ComponentStatus",
    "load_components",
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
    "LoggingCallback",
    "ProgressCallback",
    "UpdateService",
]
