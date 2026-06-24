#!/usr/bin/python3
import configparser
import hashlib
import logging
import os
import pathlib
import re
import shutil  # nosec
import subprocess  # nosec B404
import threading
from datetime import datetime
from typing import Literal

HOME = pathlib.Path.home()
CONFIG_REPO = pathlib.Path.joinpath(HOME, "RF50-Klipper")
CONFIG_DIR = pathlib.Path.joinpath(HOME, "configs")
KLIPPER_CONFIG_DIR = pathlib.Path.joinpath(HOME, "printer_data", "config")
BACKUP_DIR = pathlib.Path(HOME, ".rf50_backups")
DETECTION_CACHE = pathlib.Path.joinpath(HOME, ".rf50_config.json")
VARIABLES_FILE = pathlib.Path.joinpath(KLIPPER_CONFIG_DIR, "variables.cfg")
PRINTER_CONFIG = pathlib.Path.joinpath(KLIPPER_CONFIG_DIR, "printer.cfg")
SV_CONFIG_MARKER = "#*# <---------------------- SAVE_CONFIG ---------------------->"

_logger = logging.getLogger(__name__)


def _timestamp() -> str:
    """Return the current timestamp in ISO8601 format

    Largest unit of time to the smaller one"""
    return datetime.now().strftime("%Y-%m-%d-%H:%M:%S")


def is_git_repo(path: pathlib.Path) -> bool:
    """Check if path is a git repository by looking for the .git directory"""
    try:
        if not path.exists() or not path.is_dir():
            return False
        return (path / ".git").exists()
    except Exception:
        return False


def _run_git(path: pathlib.Path, args: list[str]) -> subprocess.CompletedProcess:
    """Run a git command with validated path (no shell)."""
    if not path.is_dir():
        raise NotADirectoryError(f"Not a directory: {path}")
    return subprocess.run(
        ["git", "-C", str(path)] + args, capture_output=True, text=True, timeout=2
    )  # nosec B603 — path validated above, no shell=True


def is_git_dirty(path: pathlib.Path | str):
    """Checks if a git repository is broken/dirty"""
    try:
        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)
        result = _run_git(path, ["status", "--porcelain"])
        if result.returncode != 0 or not result:
            return True
        return bool(result.stdout.strip())
    except Exception:
        return True


def ensure_dir(path: pathlib.Path | str) -> pathlib.Path:
    """Ensures a specified directory exists, creating the
    directory if no match was found
    """
    try:
        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)
        if not path.exists() and not path.is_dir():
            os.makedirs(path)
            _logger.info("Created missing directory %s" % path)
            return path
    except PermissionError as e:
        _logger.error(
            "Caught exception while ensuring directory %s : %s" % (path, e),
            exc_info=True,
        )
    except FileExistsError as e:
        # This will probably never be reached
        _logger.error(
            "Caught exception, directory already exists %s" % e, exc_info=True
        )
    except FileNotFoundError as e:
        _logger.error("Caught exception  %s" % e, exc_info=True)
    return pathlib.Path(path)


def check_broken_symlinks(dir: pathlib.Path) -> list[pathlib.Path]:
    """Check directory for broken symlinks

    Returns:
        list[pathlib.Path]: list of paths containing the broken symlinks
    """
    try:
        if not (dir.exists() or dir.is_dir()):
            return []
        broken: list[pathlib.Path] = []
        for path in dir.rglob("*"):
            if path.is_symlink() and not path.exists():
                broken.append(path)
        return broken
    except Exception:
        return []


def resolve_symlink(file: pathlib.Path, resolved: set[str]) -> bool:
    """Check if `file` has a valid symlink on `target` dir

    Returns:
        bool: whether or not the provided directory has a working symlink pointing to the src file
    """
    return file.resolve().as_posix() in resolved


def get_file_checksum(file: pathlib.Path | str) -> str:
    """Get file checksum

    Returns:
        str: digested file checksum
    """
    if not isinstance(file, pathlib.Path):
        file = pathlib.Path(file)
    if not file.exists():
        raise FileNotFoundError(f"File not found: {file}")
    if not file.is_file():
        raise ValueError(f"Path is not a regular file: {file}")

    try:
        with file.open("rb") as f:
            return hashlib.file_digest(f, "sha256").hexdigest()
    except OSError as e:
        _logger.error("Failed to read file for checksum %s" % e, exc_info=True)
        return ""


def copy_file_simple(orig: pathlib.Path | str, dest: pathlib.Path | str):
    """Copies a file from `orig` to `dest`"""
    if not isinstance(orig, pathlib.Path):
        orig = pathlib.Path(orig)
    if not isinstance(dest, pathlib.Path):
        dest = pathlib.Path(dest)
    if not orig.is_file() or not orig.exists():
        raise FileNotFoundError("File %s not found" % orig.as_posix())
    res = shutil.copy2(orig, dest, follow_symlinks=False)
    _logger.info("Copied file %s to destination %s" % (orig.name, dest))
    return res


class ConfigManager:
    def __init__(self, config) -> None:
        self.config = config.get_section("configuration_manager", fallback=None)

        if not self.config:
            _logger.debug("No Configuration Manager section; falling back to defaults")

        self.repo = pathlib.Path(
            (
                self.config.get("config_repo", default=CONFIG_REPO)
                if self.config
                else None
            )
            or CONFIG_REPO
        ).expanduser()
        self.mergeLock = threading.Lock()
        if not self.repo.exists() or not self.repo.is_dir():
            _logger.debug("Config repo directory %s does not exist", self.repo)
            raise NotADirectoryError("Repository directory does not exists")

        if not is_git_repo(self.repo):
            _logger.error("Provided repository directory is not a git repo")

        self.config_dir = pathlib.Path(
            (
                self.config.get("config_dir", default=KLIPPER_CONFIG_DIR)
                if self.config
                else None
            )
            or KLIPPER_CONFIG_DIR
        ).expanduser()

        if not self.config_dir.exists() or not self.config_dir.is_dir():
            _logger.error(
                "Unable to find machine configuration directory %s" % self.config_dir
            )
            raise NotADirectoryError("Machine configuration directory does not exist")

        self.backup_dir = pathlib.Path(
            (self.config.get("backup_dir", default=BACKUP_DIR) if self.config else None)
            or BACKUP_DIR
        ).expanduser()
        if not self.backup_dir.exists():
            ensure_dir(self.backup_dir)
        if not self.backup_dir.is_dir():
            raise NotADirectoryError("Provided backup dir is not a directory")

        self.config_variant = (
            self.config.get("variant", default=0) if self.config else None
        ) or 0
        self.cpy_files = (
            self.config.getlists(
                "copy_files", ["printer.cfg", "variables.cfg", "BlocksScreen.cfg"]
            )
            if self.config
            else None
        ) or ["printer.cfg", "variables.cfg", "BlocksScreen.cfg"]

        _logger.info("--- Configuration Manager Initialized --- ")
        _logger.info(
            "Configuration manager will synchronize configurations from %s to %s "
            % (
                self.repo,
                self.config_dir,
            )
        )
        _logger.info("Configuration manager will perform initial check")
        _logger.info("Configuration manager using the following details:")
        _logger.info("-> Config Directory: %s" % self.repo)
        _logger.info("-> Machine config directory: %s" % self.config_dir)
        _logger.info("-> Backup Directory: %s" % self.backup_dir)
        _logger.info("-> Config Variant: %s" % str(self.config_variant))
        _logger.info("-> Mandatory copy files: %s " % str(self.cpy_files))
        self.repo_fi_name, self.repo_fi_relpath = self._build_file_index(self.repo)
        self.config_fi_name, self.config_fi_relpath = self._build_file_index(
            self.config_dir
        )

        self.sync()

    def ensure_base_files(self, repo_dir) -> bool:
        """Check if the repository with printer configurations has
        the appropriate structure to be used in klipper.

        In this case if the repo directory has `printer.cfg` file
        and `variables.cfg` on the upper dir"""
        path = pathlib.Path(repo_dir)
        mandatory_files = ["printer.cfg", "variables.cfg", "moonraker.cfg"]
        validated = [
            pathlib.Path.joinpath(path, file).is_file() for file in mandatory_files
        ]
        return all(validated)

    @classmethod
    def cleanup_broken_symlinks(cls, root: pathlib.Path | str) -> bool:
        """Cleans up broken symlinks on specified `root` directory"""
        _cleanup_root = pathlib.Path(root)
        try:
            for i in _cleanup_root.rglob("*"):
                if i.is_symlink() and not i.resolve().exists():
                    i.unlink()
            return True
        except FileNotFoundError:
            _logger.error("Unable to find broken symbolic link for deletion")
        except ValueError:
            _logger.error("Caught fatal exception while cleaning up symbolic links")
        except (PermissionError, OSError):
            _logger.error(
                "Caught fatal exception when scanning for broken symbolic links "
            )
        return False

    def get_file_stat(self, root, file):
        """Get file stat"""
        _root = pathlib.Path(root)
        if not _root.is_dir():
            raise NotADirectoryError("Provided root directory for file does not exist")
        file_dir = _root.joinpath(file)
        if not file_dir.is_file():
            raise FileNotFoundError(f"Provided file {file} not found on {root}")
        return file_dir.stat(follow_symlinks=False)

    def _get_missing_symlinks(
        self, root: pathlib.Path | str, repo: pathlib.Path | str
    ) -> list[pathlib.Path]:
        """Scan the `root` directory for missing symbolic links compared
        against files on `repo` directory.

        Returns:
            list: paths for Missing symlinks
        """
        _root = pathlib.Path(root)
        _repo = pathlib.Path(repo)
        if not _root.is_dir() or not _root.exists():
            raise NotADirectoryError("Provided root dir missing or does not exist")
        if not _repo.is_dir() or not _repo.exists():
            raise NotADirectoryError("Provided repo dir missing or does not exist")

        _resolved: set[str] = {
            f.resolve().as_posix() for f in _root.rglob("*") if f.is_symlink()
        }
        _missing = []
        for d in _repo.rglob("*.cfg"):
            # ignore copy files
            if d.parts[-1] in self.cpy_files:
                continue
            # ignore .git dir files
            if ".git" in d.parts:
                continue
            if d.resolve().as_posix() not in _resolved:
                _missing.append(d)
        return _missing

    def _build_file_index(
        self, root: pathlib.Path
    ) -> tuple[dict[str, list[pathlib.Path]], dict[str, pathlib.Path]]:
        """Creates two lookup internal lookup tables for O(1) lookup
        of the current files"""
        tname: dict[str, list[pathlib.Path]] = {}
        trelpath: dict[str, pathlib.Path] = {}
        for f in root.rglob("*"):
            if ".git" in f.parts:
                continue
            if not f.is_file():
                continue
            rel = str(f.relative_to(root))
            trelpath[rel] = f
            tname.setdefault(f.name, []).append(f)
        return tname, trelpath

    def _symlink_config(
        self, symlink_list: list[pathlib.Path], mode: Literal[0, 1] = 0
    ) -> None:
        """Creates symbolic links for the repo configurations onto
        the machines printer configuration directory"""
        try:
            # symlinks each file, ensure correct directories
            if not mode:
                for src in symlink_list:
                    src_rel = src.relative_to(src.home())
                    target = self.config_dir / pathlib.Path(*src_rel.parts[1:])
                    if target.exists() and target.is_symlink():
                        continue
                    ensure_dir(pathlib.Path(*target.parts[:-1]))
                    target.symlink_to(src)
                return
            # TODO: Second Mode -> symlinks directories entire contents of the repo

        except Exception as e:
            _logger.error(
                "Caught exception while creating symbolic links for configuration files: %s"
                % e
            )

    def _section_blocks(self, lines):
        blocks = []
        name = None
        block = []
        for line in lines:
            m = re.match("^\[\s*(.+?)\s*\]\s*$", line)
            if m:
                if block:
                    blocks.append((name, block))
                name = m.group(1)
                block = [line]
            else:
                block.append(line)
        if block:
            blocks.append((name, block))
        return blocks

    def _parse_save_config(self, lines):
        sections = []
        name = None
        block = []
        for line in lines:
            m = re.match(r"^#\*#\s*\[\s*(.+?)\s*\]\s*$", line)
            if m:
                if block:
                    sections.append((name, block))
                name = m.group(1)
                block = [line]
            else:
                block.append(line)
        if block:
            sections.append((name, block))
        return sections

    def _parse_save_config_keys(self, block_lines):
        keys = {}
        for line in block_lines:
            m = re.match(r"^#\*#\s+(\S+)\s*=\s*(.+)$", line)
            if m:
                keys[m.group(1)] = m.group(2).strip()
        return keys

    def merge_cfg(
        self,
        src_file: pathlib.Path,
        target_file: pathlib.Path,
        marker="",
    ) -> bool:
        """Merges two configuration files together"""
        try:
            _sfl = src_file.read_text(encoding="utf-8")
            _tfl = target_file.read_text(encoding="utf-8")

            with self.mergeLock:
                if marker:
                    if marker in _tfl:
                        tfl_lines = _tfl.splitlines(keepends=True)
                        idx = next(
                            i for i, line in enumerate(tfl_lines) if marker in line
                        )
                        tgt_header = tfl_lines[:idx]
                        tgt_save = tfl_lines[idx:]  # keep as lines for merging

                        # Split source at marker too (it may or may not have one)
                        if marker in _sfl:
                            sfl_lines = _sfl.splitlines(keepends=True)
                            src_idx = next(
                                i for i, line in enumerate(sfl_lines) if marker in line
                            )
                            src_header_lines = sfl_lines[:src_idx]
                            src_save = sfl_lines[src_idx:]  # source's SAVE_CONFIG block
                        else:
                            src_header_lines = _sfl.splitlines(keepends=True)
                            src_save = []

                        # --- Merge the header (before marker) ---
                        src_blocks = self._section_blocks(src_header_lines)
                        tgt_blocks = self._section_blocks(tgt_header)

                        tgt_mcu = {
                            n: b
                            for n, b in tgt_blocks
                            if n and (n.startswith("mcu") or n.startswith("beacon"))
                        }

                        merged_header_lines = []
                        for name, block in src_blocks:
                            if (
                                name
                                and (
                                    name.startswith("mcu") or name.startswith("beacon")
                                )
                                and name in tgt_mcu
                            ):
                                merged_header_lines.extend(tgt_mcu[name])
                            else:
                                merged_header_lines.extend(block)

                        # --- Merge the SAVE_CONFIG block (after marker) ---
                        # Strategy: target wins for existing keys/sections,
                        # source contributes only new sections or new keys.
                        tgt_sc_sections = self._parse_save_config(tgt_save)
                        src_sc_sections = (
                            self._parse_save_config(src_save) if src_save else []
                        )

                        # Build a lookup of target sections by name
                        tgt_sc_map = {
                            n: block for n, block in tgt_sc_sections if n is not None
                        }
                        src_sc_map = {
                            n: block for n, block in src_sc_sections if n is not None
                        }

                        merged_save_lines = []

                        # First: emit all target sections (they take priority)
                        for name, block in tgt_sc_sections:
                            if name is None:
                                # This is the preamble (marker line + comments)
                                merged_save_lines.extend(block)
                            else:
                                merged_save_lines.extend(block)
                                # Check if source has extra keys not in target for this section
                                if name in src_sc_map:
                                    tgt_keys = self._parse_save_config_keys(block)
                                    src_keys = self._parse_save_config_keys(
                                        src_sc_map[name]
                                    )
                                    for k, v in src_keys.items():
                                        if k not in tgt_keys:
                                            merged_save_lines.append(
                                                f"#*# \t{k} = {v}\n"
                                            )

                        # Then: append any sections that exist only in source
                        for name, block in src_sc_sections:
                            if name is not None and name not in tgt_sc_map:
                                merged_save_lines.extend(block)

                        merged = "".join(merged_header_lines) + "".join(
                            merged_save_lines
                        )

                    else:
                        # Target has no SAVE_CONFIG block yet — use source as-is
                        merged = _sfl

                else:
                    src_cfg = configparser.ConfigParser(strict=False)
                    src_cfg.read_string(_sfl)
                    target_cfg = configparser.ConfigParser(strict=False)
                    if _tfl:
                        target_cfg.read_string(_tfl)

                    appendix = []
                    for section in src_cfg.sections():
                        if section.startswith("mcu") or section.startswith("beacon"):
                            continue
                        if not target_cfg.has_section(section):
                            appendix.append(
                                (section, True, list(src_cfg.items(section, raw=True)))
                            )
                        else:
                            sec_missing = [
                                (o, v)
                                for o, v in src_cfg.items(section, raw=True)
                                if not target_cfg.has_option(section, o)
                            ]
                            if sec_missing:
                                appendix.append((section, False, sec_missing))

                    for opt, val in src_cfg.defaults().items(raw=True):
                        if not target_cfg.defaults().get(opt):
                            items = (
                                appendix[-1][2]
                                if appendix and appendix[-1][0] == "DEFAULT"
                                else None
                            )
                            if items is not None:
                                items.append((opt, val))
                            else:
                                appendix.append(("DEFAULT", True, [(opt, val)]))

                    if appendix:
                        lines = []
                        for section, is_new, opts in appendix:
                            if is_new:
                                lines.append(f"[{section}]")
                            for opt, val in opts:
                                lines.append(f"{opt}: {val}")
                        text = "\n".join(lines)
                        if _tfl and not _tfl.endswith("\n"):
                            _tfl += "\n"
                        merged = _tfl + text + "\n"
                    else:
                        merged = _tfl

            if _tfl != merged:
                target_file.write_text(merged, encoding="utf-8")
            return True
        except Exception as e:
            _logger.error("Caught exception while merging: %s" % e)
            return False

    def _cpy_cfg_files(self) -> None:
        """Compares copy files with their version on the machines configuration
        if they differ, copy the updated file preserving klipper configurations"""

        try:
            if not self.cpy_files:
                _logger.info("No files configuration files to be copied")
                return

            for f in self.cpy_files:
                target = ""
                src_cpy_files = self.repo_fi_name.get(f, [])
                if not src_cpy_files:
                    _logger.info("File %s does not exist in repository " % f)
                    continue
                src_file = min(src_cpy_files, key=lambda p: len(p.parents))
                target_files = self.config_fi_name.get(f, [])
                if not target_files:
                    _src_file = src_file.relative_to(src_file.home())
                    _src_ = pathlib.Path(*_src_file.parts[1:])
                    target = self.config_dir / _src_
                    shutil.copy2(src_file, target)
                    _logger.info("File created")
                    continue

                target = min(target_files, key=lambda p: len(p.parents))
                if target.exists():
                    chk_src = get_file_checksum(src_file)
                    chk_target = get_file_checksum(target)
                    if chk_src == chk_target:
                        continue

                # Files are different so they need merging
                ok = False
                if f == "printer.cfg":
                    ok = self.merge_cfg(src_file, target, marker=SV_CONFIG_MARKER)
                elif f == "variables.cfg":
                    ok = self.merge_cfg(src_file, target)
                else:
                    ok = copy_file_simple(src_file, target)
                if not ok:
                    _logger.error("Failed to synchronize file %s" % f)
        except FileExistsError as e:
            _logger.info("Caught exception while trying to create blank file %s" % e)
        except Exception as e:
            _logger.info("Caught exception while cpy files: %s" % e)

    def cmp_file(self, src, target) -> bool:
        src = pathlib.Path(src)
        target = pathlib.Path(target)
        if not (src.exists() and src.is_file()):
            return False
        if not (target.exists() and target.is_file()):
            return False
        return get_file_checksum(src) == get_file_checksum(target)

    def cmp_cpy_files(self) -> list[bool]:
        _cmp: list[bool] = []
        for f in self.cpy_files:
            src_cpy_files = self.repo_fi_name.get(f, [])
            if not src_cpy_files:
                _cmp.append(False)
                continue
            src_file = min(src_cpy_files, key=lambda p: len(p.parents))
            target_files = self.config_fi_name.get(f, [])
            if not target_files:
                _cmp.append(False)
                continue

            target = min(target_files, key=lambda p: len(p.parents))
            if not target.exists():
                _cmp.append(False)
                continue
            chk_src = get_file_checksum(src_file)
            chk_target = get_file_checksum(target)
            _cmp.append(chk_src == chk_target)
        return _cmp

    def sync(self) -> None:
        """Synchronizes configuration repo with the
        machines configuration"""
        try:
            # self.cleanup_broken_symlinks(self.config_dir)
            _missing = self._get_missing_symlinks(self.config_dir, self.repo)
            if _missing and any(self.cmp_cpy_files()):
                self.cleanup_broken_symlinks(self.config_dir)

            self._symlink_config(_missing)
            self._cpy_cfg_files()
        except NotADirectoryError as e:
            _logger.error("%s" % e)
        except FileNotFoundError as e:
            _logger.error("%s" % e)
        except Exception as e:
            _logger.error("Caught exception: %s" % e)
