"""Device templates: which printer.cfg changes a plugged-in device requires.

Profiles come from device_profiles.yaml (bundled next to this module), merged
by name with an optional per-machine override in ~/printer_data/config. Each
profile says how to recognise a device from its /dev/serial/by-id name and
what to do to printer.cfg when it's present: create or update one section
from templated options, and comment/uncomment [include ...] lines.

Everything here is a pure text transform (only load_profiles touches the
filesystem), and every transform is idempotent: applying a profile to text
it was already applied to returns the text unchanged, so callers can apply
on every boot and every hotplug event and only write when something changed.
"""

from __future__ import annotations

import logging
import pathlib
import re
import string
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Any

import yaml
from devices.discovery.serial_devices import Device

from .configurator import SV_CONFIG_MARKER

_logger = logging.getLogger(__name__)

BUNDLED_PATH = pathlib.Path(__file__).with_name("device_profiles.yaml")
OVERRIDE_PATH = (
    pathlib.Path.home() / "printer_data" / "config" / "blockscreen_devices.yaml"
)


_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0a-\x1f\x7f]")


def _sanitize(value: str) -> str:
    """Strip control characters (newlines included) from device-derived text.

    printer.cfg is plain text where a bare newline starts a new directive:
    a device string (name/serial/path) that reaches a config line unfiltered
    could inject extra options or even a whole [section]. Values here can
    originate from the device's own USB descriptor strings, which a
    corrupted or malicious device fully controls - so this runs on every
    value before it's substituted into a template, not just on ones today's
    bundled profiles happen to use.
    """
    return _CONTROL_CHARS.sub("", value)


@dataclass(frozen=True)
class DeviceProfile:  # pylint: disable=too-many-instance-attributes
    """One device template (see device_profiles.yaml for the format)."""

    name: str
    match: re.Pattern[str]
    section: str
    options: tuple[tuple[str, str], ...] = ()
    enable_includes: tuple[str, ...] = ()
    disable_includes: tuple[str, ...] = ()
    # USB vendor/product ID (from Klipper's Kconfig USB_VENDOR_ID/USB_DEVICE_ID),
    # when the profile wants ID-based matching instead of the symlink regex.
    vendor_id: int | None = None
    product_id: int | None = None

    def matches(self, device: Device) -> bool:
        """Whether this profile applies to the given serial device.

        Prefers the USB vendor/product ID when both this profile and the
        device carry one - falls back to the symlink-name regex otherwise
        (device.vendor_id is 0 until both the daemon and the device's
        firmware report real IDs, so behaviour is unchanged until then).
        """
        if self.vendor_id is not None and device.vendor_id:
            if device.vendor_id != self.vendor_id:
                return False
            return self.product_id is None or device.product_id == self.product_id
        return re.search(self.match, device.symlink_name) is not None

    def render_options(self, device: Device) -> list[tuple[str, str]]:
        """Options with ${serial}/${device_path}/${name} filled in for device.

        The substituted values ultimately come from the device's own USB
        descriptor strings (name is built from manufacturer/product) - a
        corrupted or malicious device can put anything there, including
        control characters. _sanitize strips those so a plugged-in device
        can never inject an extra config line/section via a template value.
        """
        values = {
            "serial": _sanitize(device.symlink),
            "device_path": _sanitize(device.device_path),
            "name": _sanitize(device.name),
        }
        return [
            (key, string.Template(value).safe_substitute(values))
            for key, value in self.options
        ]


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------


def _read_entries(path: pathlib.Path) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    entries = data.get("profiles", []) if isinstance(data, dict) else []
    return [e for e in entries if isinstance(e, dict)]


def _merge(base: list[dict], override: list[dict]) -> list[dict]:
    """Merge override entries into base by name (as updater/components.py does)."""
    merged = {e["name"]: dict(e) for e in base if e.get("name")}
    for entry in override:
        name = entry.get("name")
        if not name:
            continue
        if name in merged:
            merged[name].update({k: v for k, v in entry.items() if v is not None})
        else:
            merged[name] = dict(entry)
    return list(merged.values())


def _str_list(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    return tuple(str(v) for v in value)


def _usb_id(value: Any, key: str) -> int | None:
    """Parse an optional vendor_id/product_id: int, or hex/decimal string."""
    if value is None:
        return None
    try:
        return int(value) if isinstance(value, int) else int(str(value), 0)
    except ValueError as e:
        raise ValueError(f"'{key}' must be an integer or hex string") from e


def _parse(entry: dict[str, Any]) -> DeviceProfile | None:
    name = entry.get("name")
    try:
        if not entry.get("match") or not entry.get("section"):
            raise ValueError("'match' and 'section' are required")
        options = entry.get("options") or {}
        if not isinstance(options, dict):
            raise TypeError("'options' must be a mapping")
        product_id = _usb_id(entry.get("product_id"), "product_id")
        if product_id is not None and entry.get("vendor_id") is None:
            raise ValueError("'product_id' requires 'vendor_id'")
        return DeviceProfile(
            name=str(name),
            match=re.compile(str(entry["match"]), re.IGNORECASE),
            section=" ".join(str(entry["section"]).split()),
            options=tuple((str(k), str(v)) for k, v in options.items()),
            enable_includes=_str_list(entry.get("enable_includes")),
            disable_includes=_str_list(entry.get("disable_includes")),
            vendor_id=_usb_id(entry.get("vendor_id"), "vendor_id"),
            product_id=product_id,
        )
    except (ValueError, TypeError, re.error) as e:
        _logger.error("Skipping device profile %r: %s", name, e)
        return None


def _override_is_safe(path: pathlib.Path) -> bool:
    # The override can inject arbitrary Klipper config: refuse one that
    # other users could have written, like the updater does for its own.
    try:
        mode = path.stat().st_mode
    except OSError:
        _logger.warning("Cannot stat device profile override %s, skipping", path)
        return False
    if mode & 0o022:
        _logger.warning(
            "Skipping device profile override %s: writable by group/others (mode %o)",
            path,
            mode & 0o777,
        )
        return False
    return True


def load_profiles(
    bundled: pathlib.Path = BUNDLED_PATH,
    override: pathlib.Path | None = OVERRIDE_PATH,
) -> list[DeviceProfile]:
    """Bundled profiles merged with the per-machine override, enabled ones only"""
    try:
        entries = _read_entries(bundled)
    except (OSError, yaml.YAMLError) as e:
        _logger.error("Cannot read bundled device profiles %s: %s", bundled, e)
        entries = []

    if override is not None and override.exists() and _override_is_safe(override):
        try:
            entries = _merge(entries, _read_entries(override))
            _logger.info("Device profile override applied from %s", override)
        except (OSError, yaml.YAMLError) as e:
            _logger.error("Cannot read device profile override %s: %s", override, e)

    profiles = []
    for entry in entries:
        if entry.get("enabled", True) is False:
            continue
        profile = _parse(entry)
        if profile is not None:
            profiles.append(profile)
    _warn_duplicate_ids(profiles)
    return profiles


def _warn_duplicate_ids(profiles: Sequence[DeviceProfile]) -> None:
    """Flag profiles that would both claim the same USB vendor_id/product_id.

    A copy-paste mistake in the override (or an unlucky new allocation) would
    otherwise silently apply both profiles to the same physical device - see
    USB_IDS.md for how product_id is meant to be assigned.
    """
    seen: dict[tuple[int, int | None], str] = {}
    for p in profiles:
        if p.vendor_id is None:
            continue
        key = (p.vendor_id, p.product_id)
        if key in seen:
            _logger.error(
                "Device profiles %r and %r both match vendor_id=0x%04x product_id=%s "
                "- both will apply to the same device",
                seen[key],
                p.name,
                p.vendor_id,
                f"0x{p.product_id:04x}" if p.product_id is not None else "any",
            )
        else:
            seen[key] = p.name


# --------------------------------------------------------------------------
# Text transforms
# --------------------------------------------------------------------------

_ANY_SECTION = re.compile(r"^\[[^\]]+\]")


def _section_header_re(section: str) -> re.Pattern[str]:
    words = r"\s+".join(re.escape(w) for w in section.split())
    return re.compile(rf"^\[\s*{words}\s*\]", re.IGNORECASE)


def _split_marker(text: str) -> tuple[str, str]:
    """(editable header, SAVE_CONFIG tail) - profiles never touch the tail"""
    pos = text.find(SV_CONFIG_MARKER)
    if pos < 0:
        return text, ""
    # Keep the marker's own line (and anything after) in the tail.
    line_start = text.rfind("\n", 0, pos) + 1
    return text[:line_start], text[line_start:]


def _section_span(lines: list[str], start: int) -> int:
    """Index one past the last line of the section whose header is at start"""
    end = start + 1
    while end < len(lines) and not _ANY_SECTION.match(lines[end]):
        end += 1
    return end


_MCU_SECTION = re.compile(r"^\[\s*mcu(\s[^\]]*)?\]", re.IGNORECASE)


def _insert_section(
    lines: list[str], section: str, options: Sequence[tuple[str, str]]
) -> None:
    # Just before the last [mcu ...] header, so device MCUs sit with the
    # others. Always at a section boundary, never inside a block:
    # ConfigManager.merge_cfg treats every line up to the next header as part
    # of the section above (banners included), so splitting a block would
    # make its trailing banner belong to the new section and vanish with it
    # when the device's section is dropped at the next boot.
    mcu_idxs = [i for i, line in enumerate(lines) if _MCU_SECTION.match(line)]
    if mcu_idxs:
        block = [f"[{section}]\n"] + [f"{k}: {v}\n" for k, v in options] + ["\n"]
        insert_at = mcu_idxs[-1]
    else:
        block = ["\n", f"[{section}]\n"] + [f"{k}: {v}\n" for k, v in options]
        insert_at = len(lines)
    lines[insert_at:insert_at] = block


def _update_options(
    lines: list[str], idx: int, options: Sequence[tuple[str, str]]
) -> None:
    end = _section_span(lines, idx)
    for key, value in options:
        opt_re = re.compile(rf"^(\s*){re.escape(key)}\s*[:=]\s*(.*?)\s*$")
        for i in range(idx + 1, end):
            m = opt_re.match(lines[i].rstrip("\n"))
            if m:
                if m.group(2).split("#", 1)[0].strip() != value:
                    lines[i] = f"{m.group(1)}{key}: {value}\n"
                break
        else:
            lines.insert(idx + 1, f"{key}: {value}\n")
            end += 1


def set_section_options(
    text: str, section: str, options: Sequence[tuple[str, str]]
) -> str:
    """Create [section] or update its options so each has the given value."""
    header, tail = _split_marker(text)
    lines = header.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    header_re = _section_header_re(section)
    idx = next((i for i, line in enumerate(lines) if header_re.match(line)), None)
    if idx is None:
        _insert_section(lines, section, options)
    else:
        _update_options(lines, idx, options)
    return "".join(lines) + tail


def set_include(text: str, path: str, enabled: bool) -> str:
    """Comment (enabled=False) or uncomment every [include path] line."""
    header, tail = _split_marker(text)
    # [ \t] rather than \s: \s also matches newlines, which would let `#*`
    # swallow a "#####" banner line above the include.
    include_re = re.compile(
        rf"^([ \t]*)(#*)[ \t]*(\[[ \t]*include[ \t]+{re.escape(path)}[ \t]*\].*)$",
        re.MULTILINE,
    )

    def _fix(m: re.Match[str]) -> str:
        indent, hashes, rest = m.group(1), m.group(2), m.group(3)
        if enabled:
            return f"{indent}{rest}"
        return m.group(0) if hashes else f"{indent}#{rest}"

    return include_re.sub(_fix, header) + tail


def apply_profile(text: str, profile: DeviceProfile, device: Device) -> str:
    """printer.cfg text with profile applied for device (idempotent)."""
    if profile.options:
        text = set_section_options(
            text, profile.section, profile.render_options(device)
        )
    for path in profile.enable_includes:
        text = set_include(text, path, True)
    for path in profile.disable_includes:
        text = set_include(text, path, False)
    return text


def match_devices(
    profiles: Iterable[DeviceProfile], devices: Sequence[Device]
) -> list[tuple[DeviceProfile, Device]]:
    """(profile, device) for each profile with a matching device; first match wins.

    A profile has one printer.cfg section to give, so if more than one
    connected device matches it, only the first (in `devices` order) is
    used - logged rather than silently dropping the rest, since it usually
    means two boards of the same type are plugged in at once.
    """
    pairs = []
    for profile in profiles:
        matches = [d for d in devices if profile.matches(d)]
        if not matches:
            continue
        if len(matches) > 1:
            _logger.warning(
                "Profile %r matches %d connected devices (%s); using %s, "
                "ignoring the rest",
                profile.name,
                len(matches),
                ", ".join(d.symlink_name or d.name or "?" for d in matches),
                matches[0].symlink_name or matches[0].name or "?",
            )
        pairs.append((profile, matches[0]))
    return pairs


def apply_device_profiles(
    text: str, profiles: Iterable[DeviceProfile], devices: Sequence[Device]
) -> tuple[str, list[str]]:
    """Apply every profile that has a matching device.

    Returns the new text and the names of the profiles that changed it.
    """
    changed = []
    for profile, device in match_devices(profiles, devices):
        new_text = apply_profile(text, profile, device)
        if new_text != text:
            changed.append(profile.name)
            text = new_text
    return text, changed
