#!/usr/bin/python3
import os
import pathlib
import shutil
import subprocess
import asyncio

HOME = pathlib.Path.home()
CONFIG_REPO = pathlib.Path.joinpath(HOME, "github", "RF50-Klipper")
CONFIG_DIR = pathlib.Path.joinpath(HOME, "configs")
KLIPPER_CONFIG_DIR = pathlib.Path.joinpath(HOME, "printer_data", "config")
BACKUP_DIR = pathlib.Path(HOME, ".rf50_backups")
DETECTION_CACHE = pathlib.Path.joinpath(HOME, ".rf50_config.json")
VARIABLES_FILE = pathlib.Path.joinpath(KLIPPER_CONFIG_DIR, "variables.cfg")
PRINTER_CONFIG = pathlib.Path.joinpath(KLIPPER_CONFIG_DIR, "printer.cfg")

# RF50 Printer variants
VARIANT_SYNC_V1 = "sync_v1"
VARIANT_SYNC_V2 = "sync_v2"
VARIANT_AMU = "amu"

ALL_VARIANTS = [VARIANT_SYNC_V1, VARIANT_SYNC_V2, VARIANT_AMU]


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


def resolve_symlink(directory: pathlib.Path, src: pathlib.Path) -> bool:
    """Check if file `src`has a valid symlink on the specified `directory`

    Returns:
        bool: whether or not the provided directory has a working symlink pointing to the src file
    """
    if not directory.is_dir():
        return False
    if not src.is_file():
        return False
    for dir in directory.rglob(pattern="*"):
        if os.path.islink(path=dir):
            if dir.resolve().as_posix() == src: 
                return True
    return False

class KlipperConfigManager:
    def __init__(self) -> None:

        _config_repo_exists = is_git_repo(CONFIG_REPO)
        if not _config_repo_exists:
            print("RF50-Klipper config repo does not exist.")
            exit(1)

        # self.fd = ConfigFileReader()
        self.current_variant = VARIANT_SYNC_V1

    def load(self) -> None:
        pass

    def check_variant(self) -> None:
        pass

    def build_config(self, file) -> None:
        pass

    def save_variant_to_file(self) -> None:
        # TODO: Save variant to the variables files on printer config
        pass

    def symlink_configs(self) -> None:
        pass

    def _verify_symlinks(self) -> bool:
        _bs = check_broken_symlinks(KLIPPER_CONFIG_DIR)
        return False if _bs else True


if __name__ == "__main__":
    print(is_git_repo(CONFIG_REPO))
    kc = KlipperConfigManager()
