from __future__ import annotations

import logging
import re
from pathlib import Path

from .models import ComponentConfig, ComponentStatus

__all__ = ["ComponentConfig", "ComponentStatus", "load_components"]

logger = logging.getLogger(__name__)

_SERVICE_RE = re.compile(r"^[a-zA-Z0-9@:._-]+\.service$")
_GIT_BRANCH_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._/-]*$")
_GIT_VERSION_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._/+-]*$")
_COMPONENT_NAME_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]*$")
_GIT_URL_RE = re.compile(r"^https://[a-zA-Z0-9._~:/?#\[\]@!$&'()*+,;=%-]+$")
_SERVICE_BANNED = set("/\\;&|$`") | {" ", "\t"}
OVERRIDE_PATH = Path("~/printer_data/config/blockscreen_updater.yaml").expanduser()

# Unioned into EVERY apt component: a kernel/firmware bump is unrecoverable on a 1-partition no-SSH Pi.
_KERNEL_FIRMWARE_EXCLUDES: tuple[str, ...] = (
    "^linux-image",
    "^linux-headers",
    "^raspberrypi-",
    "^firmware-",
)


def _validate_service(name: str) -> bool:
    """Return True if name is a safe, well-formed systemd .service unit name."""
    if not name:
        return False
    if any(ch in _SERVICE_BANNED for ch in name):
        return False
    return bool(_SERVICE_RE.match(name))


def _validate_component(data: dict) -> ComponentConfig | None:
    """Parse and validate a raw component dict; returns None and logs a warning on any error."""  # noqa: E501
    name = data.get("name", "")
    if not isinstance(name, str) or not name:
        logger.warning("Component missing name,  skipped")
        return None
    if len(name) > 255:
        logger.warning("Component name too long (%d chars) - skipped", len(name))
        return None
    if not _COMPONENT_NAME_RE.match(name):
        logger.warning(
            "Component %r has invalid name (must match [a-zA-Z0-9_-]+) - skipped", name
        )
        return None

    comp_type = data.get("type", "")
    if comp_type not in ("git", "apt"):
        logger.warning("Component %r has invalid type %r - skipped", name, comp_type)
        return None

    if comp_type == "git":
        raw_path = data.get("path")
        if not raw_path:
            logger.warning("Component %r missing path - skipped", name)
            return None
        resolved = Path(str(raw_path)).expanduser().resolve()
        if not resolved.is_relative_to(Path.home()):
            logger.warning("Component %r path escapes home dir - skipped", name)
            return None

        service = data.get("service")
        if service is not None and not _validate_service(str(service)):
            logger.warning(
                "Component %r has invalid service %r, skipped", name, service
            )
            return None

        branch = data.get("branch")
        if branch is not None and not _GIT_BRANCH_RE.match(str(branch)):
            logger.warning(
                "Component %r has invalid branch name %r, skipped",
                name,
                branch,
            )
            return None

        version = data.get("version")
        if version is not None and not _GIT_VERSION_RE.match(str(version)):
            logger.warning(
                "Component %r has invalid version[%s] for the branch %s",
                name,
                version,
                branch,
            )
            return None

        order = 50
        try:
            order = int(data.get("order", 50))
        except (TypeError, ValueError):
            logger.warning("Component %r has invalid order value", name)

        url = data.get("url")
        if url is not None and not _GIT_URL_RE.match(str(url)):
            logger.warning(
                "Component %r has invalid (non-https) url %r - dropping url", name, url
            )
            url = None

        reset_mode = data.get("reset_mode", "hard")
        if reset_mode not in ("hard", "soft"):
            # An unknown value must not silently take the soft path (fleet default is hard).
            logger.warning(
                "Component %r has invalid reset_mode %r - using 'hard'",
                name,
                reset_mode,
            )
            reset_mode = "hard"

        install_if_missing = bool(data.get("install_if_missing", False))
        if install_if_missing and not url:
            logger.warning(
                "Component %r sets install_if_missing but has no valid url - "
                "cannot provision, disabling",
                name,
            )
            install_if_missing = False

        return ComponentConfig(
            name=name,
            kind=comp_type,
            path=resolved,
            service=str(service) if service else None,
            reset_mode=reset_mode,
            order=order,
            branch=str(branch) if branch else None,
            version=str(version) if version else None,
            url=str(url) if url else None,
            install_if_missing=install_if_missing,
            restart_ui=bool(data.get("restart_ui", False)),
            restart_klipper=bool(data.get("restart_klipper", False)),
        )
    apt_order = 50
    try:
        apt_order = int(data.get("order", 50))
    except (TypeError, ValueError):
        logger.warning("Component %r has invalid order value", name)
    raw_exclude = data.get("apt_exclude", [])
    apt_exclude: tuple[str, ...] = ()
    if isinstance(raw_exclude, list):
        apt_exclude = tuple(str(p) for p in raw_exclude if isinstance(p, str))
    # Kernel/firmware guard is non-negotiable: prepend it, drop any duplicates.
    apt_exclude = _KERNEL_FIRMWARE_EXCLUDES + tuple(
        p for p in apt_exclude if p not in _KERNEL_FIRMWARE_EXCLUDES
    )
    return ComponentConfig(
        name=name,
        kind="apt",
        order=apt_order,
        apt_exclude=apt_exclude,
    )


def _merge(base: list[dict], override: list[dict]) -> list[dict]:
    """Merge override entries into base by name; unknown override names are appended."""
    base_by_name = {
        c["name"]: dict(c) for c in base if isinstance(c, dict) and "name" in c
    }
    for entry in override:
        if not isinstance(entry, dict):
            continue
        entry_name = entry.get("name")
        if not entry_name:
            continue
        if entry_name in base_by_name:
            for k, v in entry.items():
                if v is not None:
                    base_by_name[entry_name][k] = v
        else:
            base_by_name[entry_name] = dict(entry)
    return list(base_by_name.values())


def load_components() -> tuple[list[ComponentConfig], float]:
    """Load/validate components from bundled YAML merged with the user override.

    Returns (list of ComponentConfig, poll_interval in seconds).
    """
    try:
        import yaml  # noqa: PLC0415
    except ImportError:
        logger.error("PyYAML not installed; updater unavailable until next restart")  # noqa: TRY400
        return [], 1440 * 60.0

    bundled_path = Path(__file__).parent / "components.yaml"
    try:
        with open(bundled_path) as f:  # noqa: PTH123
            bundled_data = yaml.safe_load(f)
    except OSError:
        logger.exception("bundled_data not found")
        return [], 1440 * 60.0
    except yaml.YAMLError:
        logger.exception("Malformed YAML file")
        return [], 1440 * 60.0

    if not isinstance(bundled_data, dict):
        logger.error("Data is empty")
        return [], 1440 * 60.0
    raw_components: list[dict] = bundled_data.get("components", [])

    try:
        override_exists = OVERRIDE_PATH.exists()
    except OSError:
        override_exists = False
        logger.warning("Cannot access override path %s", OVERRIDE_PATH)

    if override_exists:
        try:
            stat = OVERRIDE_PATH.stat()
            if stat.st_mode & 0o022:
                logger.warning(
                    "Skipping override %s: writable by group/others (mode %o)",
                    OVERRIDE_PATH,
                    stat.st_mode & 0o777,
                )
                override_exists = False
        except OSError:
            logger.warning("Cannot stat override path %s - skipping", OVERRIDE_PATH)
            override_exists = False

    if override_exists:
        try:
            with open(OVERRIDE_PATH) as f:  # noqa: PTH123
                override_data = yaml.safe_load(f)
            if isinstance(override_data, dict):
                raw_components = _merge(
                    raw_components,
                    override_data.get("components", []),
                )
        except Exception:
            logger.exception("Failed to load override YAML %s", OVERRIDE_PATH)
    configs: list[ComponentConfig] = []
    for entry in raw_components:
        if not isinstance(entry, dict):
            logger.warning("Component entry is not a mapping - skipped: %r", entry)
            continue
        cfg = _validate_component(entry)
        if cfg is not None:
            configs.append(cfg)
    # Auto-inject system apt component if none configured in YAML.
    if not any(c.kind == "apt" for c in configs):
        configs.insert(
            0,
            ComponentConfig(
                name="system",
                kind="apt",
                order=1,
                apt_exclude=_KERNEL_FIRMWARE_EXCLUDES,
            ),
        )
    try:
        poll_seconds = float(bundled_data.get("poll_interval_minutes", 1440)) * 60.0
    except (TypeError, ValueError):
        logger.warning("Invalid poll_interval_minutes - using 1440")
        poll_seconds = 1440 * 60.0
    configs.sort(key=lambda c: c.order)
    return configs, poll_seconds
