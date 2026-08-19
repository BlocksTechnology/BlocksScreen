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
_HEALTH_URL_RE = re.compile(
    r"^http://(127\.0\.0\.1|localhost)(:\d{1,5})?/[a-zA-Z0-9._~:/?#\[\]@!$&'()*+,;=%-]*$"
)
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


def _parse_order(name: str, data: dict) -> int:
    """Parse the integer 'order' field, defaulting to 50 on any bad value."""
    try:
        return int(data.get("order", 50))
    except (TypeError, ValueError):
        logger.warning("Component %r has invalid order value", name)
        return 50


def _parse_git_branch(name: str, raw_branch: object) -> tuple[str | None, bool]:
    """Normalize/validate a git branch (strip 'origin/'); (branch, ok=False) on invalid."""
    if raw_branch is None:
        return None, True
    branch = str(raw_branch)
    # Strip a stray remote prefix: `origin/x` would fetch `origin/origin/x`.
    if branch.startswith("origin/"):
        logger.warning(
            "Component %r branch %r has an 'origin/' prefix - stripping it",
            name,
            branch,
        )
        branch = branch[len("origin/") :]
    if not _GIT_BRANCH_RE.match(branch):
        logger.warning("Component %r has invalid branch name %r, skipped", name, branch)
        return None, False
    return branch, True


def _parse_git_url(name: str, url: object) -> object:
    """Validate the https url; drop it (None) on any non-https value."""
    if url is not None and not _GIT_URL_RE.match(str(url)):
        logger.warning(
            "Component %r has invalid (non-https) url %r - dropping url", name, url
        )
        return None
    return url


def _parse_health_url(name: str, url: object) -> str | None:
    """Accept only a loopback http readiness URL; drop anything else."""
    if url is None:
        return None
    if not _HEALTH_URL_RE.match(str(url)):
        logger.warning(
            "Component %r has non-loopback health_url %r - dropping", name, url
        )
        return None
    return str(url)


def _parse_reset_mode(name: str, reset_mode: object) -> str:
    """Return 'hard'/'soft'; unknown values fall back to 'hard' (fleet default)."""
    if reset_mode not in ("hard", "soft"):
        # An unknown value must not silently take the soft path (fleet default is hard).
        logger.warning(
            "Component %r has invalid reset_mode %r - using 'hard'",
            name,
            reset_mode,
        )
        return "hard"
    return str(reset_mode)


def _validate_git_component(name: str, data: dict) -> ComponentConfig | None:
    """Parse/validate a git component dict; None on any invalid field."""
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
        logger.warning("Component %r has invalid service %r, skipped", name, service)
        return None

    branch, branch_ok = _parse_git_branch(name, data.get("branch"))
    if not branch_ok:
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

    order = _parse_order(name, data)
    url = _parse_git_url(name, data.get("url"))
    reset_mode = _parse_reset_mode(name, data.get("reset_mode", "hard"))

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
        kind="git",
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
        health_url=_parse_health_url(name, data.get("health_url")),
    )


def _validate_apt_component(name: str, data: dict) -> ComponentConfig:
    """Build an apt ComponentConfig, always unioning the kernel/firmware excludes."""
    apt_order = _parse_order(name, data)
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
        return _validate_git_component(name, data)
    return _validate_apt_component(name, data)


def _merge(base: list[dict], override: list[dict]) -> list[dict]:
    """Merge override entries into base by name; unknown override names are appended."""
    base_by_name = {
        c["name"]: c.copy() for c in base if isinstance(c, dict) and "name" in c
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
            base_by_name[entry_name] = entry.copy()
    return list(base_by_name.values())


def _load_bundled_yaml(yaml) -> dict | None:
    """Read + parse the bundled components.yaml; None on any read/parse error."""
    bundled_path = Path(__file__).parent / "components.yaml"
    try:
        with open(bundled_path) as f:  # noqa: PTH123
            bundled_data = yaml.safe_load(f)
    except OSError:
        logger.exception("bundled_data not found")
        return None
    except yaml.YAMLError:
        logger.exception("Malformed YAML file")
        return None
    if not isinstance(bundled_data, dict):
        logger.error("Data is empty")
        return None
    return bundled_data


def _load_override(raw_components: list[dict], yaml) -> list[dict]:
    """Merge the user override YAML into raw_components (skips unsafe/malformed overrides)."""
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
    return raw_components


def _build_configs(raw_components: list[dict]) -> list[ComponentConfig]:
    """Validate each raw entry, then auto-inject a system apt component if none exists."""
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
    return configs


def load_components() -> tuple[list[ComponentConfig], float]:
    """Load/validate components from bundled YAML merged with the user override."""
    try:
        import yaml  # noqa: PLC0415

        # A truncated install (interrupted pip, power cut) still imports but exposes only dunders.
        _ = (yaml.safe_load, yaml.YAMLError)
    except (ImportError, AttributeError):
        logger.exception("PyYAML missing or broken; updater idle until venv repair")
        return [], 1440 * 60.0

    bundled_data = _load_bundled_yaml(yaml)
    if bundled_data is None:
        return [], 1440 * 60.0
    raw_components: list[dict] = bundled_data.get("components", [])
    raw_components = _load_override(raw_components, yaml)
    configs = _build_configs(raw_components)
    try:
        poll_seconds = float(bundled_data.get("poll_interval_minutes", 1440)) * 60.0
    except (TypeError, ValueError):
        logger.warning("Invalid poll_interval_minutes - using 1440")
        poll_seconds = 1440 * 60.0
    configs.sort(key=lambda c: c.order)
    return configs, poll_seconds
