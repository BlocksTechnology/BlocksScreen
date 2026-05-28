#!/usr/bin/python3
import asyncio
import hashlib
import configparser
import io
import logging
import os
import pathlib
import re
import shutil
import subprocess
import threading
from datetime import datetime
from io import StringIO, TextIOWrapper
from typing import Literal

HOME = pathlib.Path.home()
CONFIG_REPO = pathlib.Path.joinpath(HOME, "github", "RF50-Klipper")
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
    """https://stackoverflow.com/questions/19687394/python-script-to-determine-if-a-directory-is-a-git-repository"""
    try:
        if not (path.exists() or path.is_dir()):
            return False
        _existance = (
            bool(
                subprocess.call(
                    ["git", "-C", path, "status"],
                    stderr=subprocess.STDOUT,
                    stdout=open(os.devnull, "w"),
                )
            )
            == 0
        )
        return _existance
    except Exception:
        return False


def is_git_dirty(path: pathlib.Path | str):
    """Checks if a git repository is broken/dirty"""
    try:
        if not isinstance(path, pathlib.Path):
            path = pathlib.Path(path)
        if not path.is_dir() or not path.exists():
            raise NotADirectoryError(
                "Provides repo dir %s was not found or is not a directory" % path
            )
        result = subprocess.run(
            ["git", "-C", str(path), "status", "--porcelain"],
            capture_output=True,
            text=True,
        )
        return bool(result.stdout.strip())
    except Exception:
        return True


def ensure_dir(path: pathlib.Path | str) -> pathlib.Path:
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


def resolve_symlink(file: pathlib.Path, target: pathlib.Path) -> bool:
    """Check if `file` has a valid symlink on `target` dir

    Returns:
        bool: whether or not the provided directory has a working symlink pointing to the src file
    """
    if not target.is_dir():
        return False
    for f in target.rglob(pattern="*"):
        if file.resolve().as_posix() == f.resolve().as_posix():
            return True
    return False


def get_file_checksum(file: pathlib.Path | str) -> str:
    if not isinstance(file, pathlib.Path):
        file = pathlib.Path(file)
    try:
        if not file.is_file() or not file.exists():
            raise FileNotFoundError(
                "Unable to find file %s while creating checksum" % file
            )
        with open(file, "rb") as f:
            digest = hashlib.file_digest(f, "sha256")
            return digest.hexdigest()
    except Exception as e:
        _logger.error("Caught fatal exception while hashing file %s" % e, exc_info=True)
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
        self.repo = pathlib.Path(
            self.config.get("config_repo", default="")
        ).expanduser()
        self.mergeLock = threading.Lock()
        if not self.repo:
            _logger.error(
                "No valid configuration repository for configuration manager. Ignoring module."
            )

        if not self.repo.exists() or not self.repo.is_dir():
            _logger.error("Repo directory does not exist")
            raise NotADirectoryError("Repository directory does not exits")

        if not is_git_repo(self.repo):
            _logger.error("Provided repository directory is not a git repo")

        self.config_dir = pathlib.Path(
            self.config.get("config_dir", default=KLIPPER_CONFIG_DIR)
        ).expanduser()
        if not self.config_dir.exists() or not self.config_dir.is_dir():
            _logger.error(
                "Unable to find machine configuration directory %s" % self.config_dir
            )
            raise NotADirectoryError("Machine configuration directory does not exist")

        self.backup_dir = pathlib.Path(
            self.config.get("backup_dir", default=BACKUP_DIR)
        ).expanduser()
        if not self.backup_dir.exists():
            ensure_dir(self.backup_dir)
        if not self.backup_dir.is_dir():
            raise NotADirectoryError("Provided backup dir is not a directory")

        self.config_variant = self.config.get("variant", default=0)
        self.cpy_files = self.config.getlists(
            "copy_files", ["printer.cfg", "variables.cfg", "BlocksScreen.cfg"]
        )

        _logger.info(self.cpy_files)
        _logger.info("--- Configuration Manager Initialized --- ")
        _logger.info(
            "Configuration manager will synchronyze configurations from %s to %s "
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
            _logger.error("Unable to find broken symbolic link for deletetion")
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
        againts files on `repo` directory.

        Returns:
            list: paths for Missing symlinks
        """
        _root = pathlib.Path(root)
        _repo = pathlib.Path(repo)
        if not _root.is_dir() or not _root.exists():
            raise NotADirectoryError("Provided root dir missig or does not exist")
        if not _repo.is_dir() or not _repo.exists():
            raise NotADirectoryError("Provided repo dir missing or does not exist")

        _missing = []
        for d in _repo.rglob("*.cfg"):
            # ignore copy files
            if d.parts[-1] in self.cpy_files:
                continue
            # ignore .git dir files
            if ".git" in d.parts:
                continue
            valid = resolve_symlink(d, _root)
            if not valid:
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

    def merge_cfg(
        self,
        src_file: pathlib.Path,
        target_file: pathlib.Path,
        marker="",
    ) -> bool:
        try:
            _sfl = src_file.read_text(encoding="utf-8")
            _tfl = target_file.read_text(encoding="utf-8")
            with self.mergeLock:
                if marker:
                    if marker in _tfl:
                        tfl_lines = _tfl.splitlines(keepends=True)
                        idx = next(i for i, l in enumerate(tfl_lines) if marker in l)
                        tgt_header = tfl_lines[:idx]
                        tgt_save = "".join(tfl_lines[idx:])

                        def _section_blocks(lines):
                            blocks = []
                            name = None
                            block = []
                            for line in lines:
                                m = re.match(r'^\[\s*(.+?)\s*\]\s*$', line)
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

                        src_blocks = _section_blocks(_sfl.splitlines(keepends=True))
                        tgt_blocks = _section_blocks(tgt_header)

                        tgt_mcu = {n: b for n, b in tgt_blocks if n and n.startswith("mcu")}

                        merged_lines = []
                        for name, block in src_blocks:
                            if name and name.startswith("mcu") and name in tgt_mcu:
                                merged_lines.extend(tgt_mcu[name])
                            else:
                                merged_lines.extend(block)

                        merged = "".join(merged_lines) + tgt_save
                    else:
                        merged = _sfl
                else:
                    src_cfg = configparser.ConfigParser(strict=False)
                    src_cfg.read_string(_sfl)
                    target_cfg = configparser.ConfigParser(strict=False)
                    if _tfl:
                        target_cfg.read_string(_tfl)

                    appendix = []
                    for section in src_cfg.sections():
                        if section.startswith("mcu"):
                            continue
                        if not target_cfg.has_section(section):
                            appendix.append((section, True, list(src_cfg.items(section))))
                        else:
                            sec_missing = [
                                (o, v) for o, v in src_cfg.items(section)
                                if not target_cfg.has_option(section, o)
                            ]
                            if sec_missing:
                                appendix.append((section, False, sec_missing))

                    for opt, val in src_cfg.defaults().items():
                        if not target_cfg.defaults().get(opt):
                            items = appendix[-1][2] if appendix and appendix[-1][0] == "DEFAULT" else None
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
        if they differ, copy the udpdated file perserving klipper configurations"""

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

    def sync(self) -> None:
        """Synchronizes configuration repo with the
        machines configuration"""
        try:
            self.cleanup_broken_symlinks(self.config_dir)
            _missing = self._get_missing_symlinks(self.config_dir, self.repo)
            self._symlink_config(_missing)


            self._cpy_cfg_files()
        except NotADirectoryError as e:
            _logger.error("%s" % e)
        except FileNotFoundError as e:
            _logger.error("%s" % e)
        except Exception as e:
            _logger.error("Caught exception: %s" % e)
