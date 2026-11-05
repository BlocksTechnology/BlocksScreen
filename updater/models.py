from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class ComponentConfig:
    """One components.yaml entry; restart_ui/restart_klipper add that restart."""

    name: str
    kind: str
    path: Path | None = None
    service: str | None = None
    reset_mode: str = "hard"
    order: int = 50
    branch: str | None = None
    version: str | None = None
    apt_exclude: tuple[str, ...] = ()
    url: str | None = None
    install_if_missing: bool = False
    restart_ui: bool = False
    restart_klipper: bool = False
    health_url: str | None = None


@dataclass(frozen=True)
class ComponentStatus:
    """Point-in-time update status of one component."""

    name: str
    kind: str = "git"
    commits_behind: int = 0
    current_hash: str = ""
    current_version: str = ""
    remote_version: str = ""
    remote_url: str = ""
    packages_upgradable: int = 0
    error: str | None = None
    has_local_changes: bool = False
    needs_install: bool = False
    branch_mismatch: bool = False
    current_branch: str = ""

    @property
    def needs_update(self) -> bool:
        """Dirty for update_all: errored git repos count (update self-heals them), apt errors don't."""
        return bool(
            self.commits_behind
            or self.packages_upgradable > 0
            or self.has_local_changes
            or self.needs_install
            or self.branch_mismatch
            or (self.error is not None and self.kind != "apt")
        )
