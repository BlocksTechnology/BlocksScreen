import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)

AMU_FILES: list[str] = [
    "mmu/base/*.cfg",
    "mmu/optional/client_macros.cfg",
    "filament_manager.cfg",
]

_AMU_PATTERNS: list[re.Pattern[str]] = [
    re.compile(rf"^(#?)(\[include {re.escape(f)}\])", re.MULTILINE) for f in AMU_FILES
]
from typing import Annotated
from typing import Callable
from typing import ClassVar

MutantDict = Annotated[dict[str, Callable], "Mutant"] # type: ignore


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None): # type: ignore
    """Forward call to original or mutated function, depending on the environment"""
    import os # type: ignore
    mutant_under_test = os.environ['MUTANT_UNDER_TEST'] # type: ignore
    if mutant_under_test == 'fail': # type: ignore
        from mutmut.__main__ import MutmutProgrammaticFailException # type: ignore
        raise MutmutProgrammaticFailException('Failed programmatically')       # type: ignore
    elif mutant_under_test == 'stats': # type: ignore
        from mutmut.__main__ import record_trampoline_hit # type: ignore
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__) # type: ignore
        # (for class methods, orig is bound and thus does not need the explicit self argument)
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_' # type: ignore
    if not mutant_under_test.startswith(prefix): # type: ignore
        result = orig(*call_args, **call_kwargs) # type: ignore
        return result # type: ignore
    mutant_name = mutant_under_test.rpartition('.')[-1] # type: ignore
    if self_arg is not None: # type: ignore
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs) # type: ignore
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs) # type: ignore
    return result # type: ignore


class ConfigToggler:
    """Manages commenting/uncommenting AMU cfg includes in printer.cfg"""

    def __init__(self, config_path: Path) -> None:
        args = [config_path]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁConfigTogglerǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁConfigTogglerǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁConfigTogglerǁ__init____mutmut_orig(self, config_path: Path) -> None:
        """Store path, detects current state from file"""
        self._path: Path | None = None
        self._state: bool = False
        if config_path.exists():
            self._path = config_path
            self._state = self._detect_state()
        else:
            logger.warning("Config File not found %s", config_path)

    def xǁConfigTogglerǁ__init____mutmut_1(self, config_path: Path) -> None:
        """Store path, detects current state from file"""
        self._path: Path | None = ""
        self._state: bool = False
        if config_path.exists():
            self._path = config_path
            self._state = self._detect_state()
        else:
            logger.warning("Config File not found %s", config_path)

    def xǁConfigTogglerǁ__init____mutmut_2(self, config_path: Path) -> None:
        """Store path, detects current state from file"""
        self._path: Path | None = None
        self._state: bool = None
        if config_path.exists():
            self._path = config_path
            self._state = self._detect_state()
        else:
            logger.warning("Config File not found %s", config_path)

    def xǁConfigTogglerǁ__init____mutmut_3(self, config_path: Path) -> None:
        """Store path, detects current state from file"""
        self._path: Path | None = None
        self._state: bool = True
        if config_path.exists():
            self._path = config_path
            self._state = self._detect_state()
        else:
            logger.warning("Config File not found %s", config_path)

    def xǁConfigTogglerǁ__init____mutmut_4(self, config_path: Path) -> None:
        """Store path, detects current state from file"""
        self._path: Path | None = None
        self._state: bool = False
        if config_path.exists():
            self._path = None
            self._state = self._detect_state()
        else:
            logger.warning("Config File not found %s", config_path)

    def xǁConfigTogglerǁ__init____mutmut_5(self, config_path: Path) -> None:
        """Store path, detects current state from file"""
        self._path: Path | None = None
        self._state: bool = False
        if config_path.exists():
            self._path = config_path
            self._state = None
        else:
            logger.warning("Config File not found %s", config_path)

    def xǁConfigTogglerǁ__init____mutmut_6(self, config_path: Path) -> None:
        """Store path, detects current state from file"""
        self._path: Path | None = None
        self._state: bool = False
        if config_path.exists():
            self._path = config_path
            self._state = self._detect_state()
        else:
            logger.warning(None, config_path)

    def xǁConfigTogglerǁ__init____mutmut_7(self, config_path: Path) -> None:
        """Store path, detects current state from file"""
        self._path: Path | None = None
        self._state: bool = False
        if config_path.exists():
            self._path = config_path
            self._state = self._detect_state()
        else:
            logger.warning("Config File not found %s", None)

    def xǁConfigTogglerǁ__init____mutmut_8(self, config_path: Path) -> None:
        """Store path, detects current state from file"""
        self._path: Path | None = None
        self._state: bool = False
        if config_path.exists():
            self._path = config_path
            self._state = self._detect_state()
        else:
            logger.warning(config_path)

    def xǁConfigTogglerǁ__init____mutmut_9(self, config_path: Path) -> None:
        """Store path, detects current state from file"""
        self._path: Path | None = None
        self._state: bool = False
        if config_path.exists():
            self._path = config_path
            self._state = self._detect_state()
        else:
            logger.warning("Config File not found %s", )

    def xǁConfigTogglerǁ__init____mutmut_10(self, config_path: Path) -> None:
        """Store path, detects current state from file"""
        self._path: Path | None = None
        self._state: bool = False
        if config_path.exists():
            self._path = config_path
            self._state = self._detect_state()
        else:
            logger.warning("XXConfig File not found %sXX", config_path)

    def xǁConfigTogglerǁ__init____mutmut_11(self, config_path: Path) -> None:
        """Store path, detects current state from file"""
        self._path: Path | None = None
        self._state: bool = False
        if config_path.exists():
            self._path = config_path
            self._state = self._detect_state()
        else:
            logger.warning("config file not found %s", config_path)

    def xǁConfigTogglerǁ__init____mutmut_12(self, config_path: Path) -> None:
        """Store path, detects current state from file"""
        self._path: Path | None = None
        self._state: bool = False
        if config_path.exists():
            self._path = config_path
            self._state = self._detect_state()
        else:
            logger.warning("CONFIG FILE NOT FOUND %S", config_path)
    
    xǁConfigTogglerǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁConfigTogglerǁ__init____mutmut_1': xǁConfigTogglerǁ__init____mutmut_1, 
        'xǁConfigTogglerǁ__init____mutmut_2': xǁConfigTogglerǁ__init____mutmut_2, 
        'xǁConfigTogglerǁ__init____mutmut_3': xǁConfigTogglerǁ__init____mutmut_3, 
        'xǁConfigTogglerǁ__init____mutmut_4': xǁConfigTogglerǁ__init____mutmut_4, 
        'xǁConfigTogglerǁ__init____mutmut_5': xǁConfigTogglerǁ__init____mutmut_5, 
        'xǁConfigTogglerǁ__init____mutmut_6': xǁConfigTogglerǁ__init____mutmut_6, 
        'xǁConfigTogglerǁ__init____mutmut_7': xǁConfigTogglerǁ__init____mutmut_7, 
        'xǁConfigTogglerǁ__init____mutmut_8': xǁConfigTogglerǁ__init____mutmut_8, 
        'xǁConfigTogglerǁ__init____mutmut_9': xǁConfigTogglerǁ__init____mutmut_9, 
        'xǁConfigTogglerǁ__init____mutmut_10': xǁConfigTogglerǁ__init____mutmut_10, 
        'xǁConfigTogglerǁ__init____mutmut_11': xǁConfigTogglerǁ__init____mutmut_11, 
        'xǁConfigTogglerǁ__init____mutmut_12': xǁConfigTogglerǁ__init____mutmut_12
    }
    xǁConfigTogglerǁ__init____mutmut_orig.__name__ = 'xǁConfigTogglerǁ__init__'

    def _detect_state(self) -> bool:
        args = []# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁConfigTogglerǁ_detect_state__mutmut_orig'), object.__getattribute__(self, 'xǁConfigTogglerǁ_detect_state__mutmut_mutants'), args, kwargs, self)

    def xǁConfigTogglerǁ_detect_state__mutmut_orig(self) -> bool:
        if self._path is None:
            return False
        try:
            text = self._path.read_text()
            return all(
                re.search(rf"^\[include {re.escape(f)}\]", text, re.MULTILINE)
                for f in AMU_FILES
            )
        except OSError:
            return False

    def xǁConfigTogglerǁ_detect_state__mutmut_1(self) -> bool:
        if self._path is not None:
            return False
        try:
            text = self._path.read_text()
            return all(
                re.search(rf"^\[include {re.escape(f)}\]", text, re.MULTILINE)
                for f in AMU_FILES
            )
        except OSError:
            return False

    def xǁConfigTogglerǁ_detect_state__mutmut_2(self) -> bool:
        if self._path is None:
            return True
        try:
            text = self._path.read_text()
            return all(
                re.search(rf"^\[include {re.escape(f)}\]", text, re.MULTILINE)
                for f in AMU_FILES
            )
        except OSError:
            return False

    def xǁConfigTogglerǁ_detect_state__mutmut_3(self) -> bool:
        if self._path is None:
            return False
        try:
            text = None
            return all(
                re.search(rf"^\[include {re.escape(f)}\]", text, re.MULTILINE)
                for f in AMU_FILES
            )
        except OSError:
            return False

    def xǁConfigTogglerǁ_detect_state__mutmut_4(self) -> bool:
        if self._path is None:
            return False
        try:
            text = self._path.read_text()
            return all(
                None
            )
        except OSError:
            return False

    def xǁConfigTogglerǁ_detect_state__mutmut_5(self) -> bool:
        if self._path is None:
            return False
        try:
            text = self._path.read_text()
            return all(
                re.search(None, text, re.MULTILINE)
                for f in AMU_FILES
            )
        except OSError:
            return False

    def xǁConfigTogglerǁ_detect_state__mutmut_6(self) -> bool:
        if self._path is None:
            return False
        try:
            text = self._path.read_text()
            return all(
                re.search(rf"^\[include {re.escape(f)}\]", None, re.MULTILINE)
                for f in AMU_FILES
            )
        except OSError:
            return False

    def xǁConfigTogglerǁ_detect_state__mutmut_7(self) -> bool:
        if self._path is None:
            return False
        try:
            text = self._path.read_text()
            return all(
                re.search(rf"^\[include {re.escape(f)}\]", text, None)
                for f in AMU_FILES
            )
        except OSError:
            return False

    def xǁConfigTogglerǁ_detect_state__mutmut_8(self) -> bool:
        if self._path is None:
            return False
        try:
            text = self._path.read_text()
            return all(
                re.search(text, re.MULTILINE)
                for f in AMU_FILES
            )
        except OSError:
            return False

    def xǁConfigTogglerǁ_detect_state__mutmut_9(self) -> bool:
        if self._path is None:
            return False
        try:
            text = self._path.read_text()
            return all(
                re.search(rf"^\[include {re.escape(f)}\]", re.MULTILINE)
                for f in AMU_FILES
            )
        except OSError:
            return False

    def xǁConfigTogglerǁ_detect_state__mutmut_10(self) -> bool:
        if self._path is None:
            return False
        try:
            text = self._path.read_text()
            return all(
                re.search(rf"^\[include {re.escape(f)}\]", text, )
                for f in AMU_FILES
            )
        except OSError:
            return False

    def xǁConfigTogglerǁ_detect_state__mutmut_11(self) -> bool:
        if self._path is None:
            return False
        try:
            text = self._path.read_text()
            return all(
                re.search(rf"^\[include {re.escape(None)}\]", text, re.MULTILINE)
                for f in AMU_FILES
            )
        except OSError:
            return False

    def xǁConfigTogglerǁ_detect_state__mutmut_12(self) -> bool:
        if self._path is None:
            return False
        try:
            text = self._path.read_text()
            return all(
                re.search(rf"^\[include {re.escape(f)}\]", text, re.MULTILINE)
                for f in AMU_FILES
            )
        except OSError:
            return True
    
    xǁConfigTogglerǁ_detect_state__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁConfigTogglerǁ_detect_state__mutmut_1': xǁConfigTogglerǁ_detect_state__mutmut_1, 
        'xǁConfigTogglerǁ_detect_state__mutmut_2': xǁConfigTogglerǁ_detect_state__mutmut_2, 
        'xǁConfigTogglerǁ_detect_state__mutmut_3': xǁConfigTogglerǁ_detect_state__mutmut_3, 
        'xǁConfigTogglerǁ_detect_state__mutmut_4': xǁConfigTogglerǁ_detect_state__mutmut_4, 
        'xǁConfigTogglerǁ_detect_state__mutmut_5': xǁConfigTogglerǁ_detect_state__mutmut_5, 
        'xǁConfigTogglerǁ_detect_state__mutmut_6': xǁConfigTogglerǁ_detect_state__mutmut_6, 
        'xǁConfigTogglerǁ_detect_state__mutmut_7': xǁConfigTogglerǁ_detect_state__mutmut_7, 
        'xǁConfigTogglerǁ_detect_state__mutmut_8': xǁConfigTogglerǁ_detect_state__mutmut_8, 
        'xǁConfigTogglerǁ_detect_state__mutmut_9': xǁConfigTogglerǁ_detect_state__mutmut_9, 
        'xǁConfigTogglerǁ_detect_state__mutmut_10': xǁConfigTogglerǁ_detect_state__mutmut_10, 
        'xǁConfigTogglerǁ_detect_state__mutmut_11': xǁConfigTogglerǁ_detect_state__mutmut_11, 
        'xǁConfigTogglerǁ_detect_state__mutmut_12': xǁConfigTogglerǁ_detect_state__mutmut_12
    }
    xǁConfigTogglerǁ_detect_state__mutmut_orig.__name__ = 'xǁConfigTogglerǁ_detect_state'

    def toggle(self, activate: bool) -> bool:
        args = [activate]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁConfigTogglerǁtoggle__mutmut_orig'), object.__getattribute__(self, 'xǁConfigTogglerǁtoggle__mutmut_mutants'), args, kwargs, self)

    def xǁConfigTogglerǁtoggle__mutmut_orig(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_1(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is not None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_2(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning(None)
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_3(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("XXNo Config File availableXX")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_4(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("no config file available")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_5(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("NO CONFIG FILE AVAILABLE")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_6(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return True
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_7(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state != activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_8(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return True
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_9(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = None
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_10(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = r"XX\2XX" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_11(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"XX#\2XX"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_12(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = None
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_13(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = None
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_14(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(None, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_15(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, None)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_16(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_17(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, )
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_18(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(None)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_19(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = None
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_20(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return False
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_21(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                None, activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_22(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", None, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_23(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate, None
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_24(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_25(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_26(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate, )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_27(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "XXConfigToggler.toggle(activate=%s): read/write failed: %sXX", activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_28(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "configtoggler.toggle(activate=%s): read/write failed: %s", activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_29(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "CONFIGTOGGLER.TOGGLE(ACTIVATE=%S): READ/WRITE FAILED: %S", activate, e
            )
            return False

    def xǁConfigTogglerǁtoggle__mutmut_30(self, activate: bool) -> bool:
        """Comment or uncomment AMU includes. Returns True on success, False on no-op or error."""
        if self._path is None:
            logger.warning("No Config File available")
            return False
        if self._state == activate:
            return False
        replacement = r"\2" if activate else r"#\2"
        try:
            text = self._path.read_text()
            for pattern in _AMU_PATTERNS:
                text = pattern.sub(replacement, text)
            self._path.write_text(text)
            self._state = activate
            return True
        except OSError as e:
            logger.error(
                "ConfigToggler.toggle(activate=%s): read/write failed: %s", activate, e
            )
            return True
    
    xǁConfigTogglerǁtoggle__mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁConfigTogglerǁtoggle__mutmut_1': xǁConfigTogglerǁtoggle__mutmut_1, 
        'xǁConfigTogglerǁtoggle__mutmut_2': xǁConfigTogglerǁtoggle__mutmut_2, 
        'xǁConfigTogglerǁtoggle__mutmut_3': xǁConfigTogglerǁtoggle__mutmut_3, 
        'xǁConfigTogglerǁtoggle__mutmut_4': xǁConfigTogglerǁtoggle__mutmut_4, 
        'xǁConfigTogglerǁtoggle__mutmut_5': xǁConfigTogglerǁtoggle__mutmut_5, 
        'xǁConfigTogglerǁtoggle__mutmut_6': xǁConfigTogglerǁtoggle__mutmut_6, 
        'xǁConfigTogglerǁtoggle__mutmut_7': xǁConfigTogglerǁtoggle__mutmut_7, 
        'xǁConfigTogglerǁtoggle__mutmut_8': xǁConfigTogglerǁtoggle__mutmut_8, 
        'xǁConfigTogglerǁtoggle__mutmut_9': xǁConfigTogglerǁtoggle__mutmut_9, 
        'xǁConfigTogglerǁtoggle__mutmut_10': xǁConfigTogglerǁtoggle__mutmut_10, 
        'xǁConfigTogglerǁtoggle__mutmut_11': xǁConfigTogglerǁtoggle__mutmut_11, 
        'xǁConfigTogglerǁtoggle__mutmut_12': xǁConfigTogglerǁtoggle__mutmut_12, 
        'xǁConfigTogglerǁtoggle__mutmut_13': xǁConfigTogglerǁtoggle__mutmut_13, 
        'xǁConfigTogglerǁtoggle__mutmut_14': xǁConfigTogglerǁtoggle__mutmut_14, 
        'xǁConfigTogglerǁtoggle__mutmut_15': xǁConfigTogglerǁtoggle__mutmut_15, 
        'xǁConfigTogglerǁtoggle__mutmut_16': xǁConfigTogglerǁtoggle__mutmut_16, 
        'xǁConfigTogglerǁtoggle__mutmut_17': xǁConfigTogglerǁtoggle__mutmut_17, 
        'xǁConfigTogglerǁtoggle__mutmut_18': xǁConfigTogglerǁtoggle__mutmut_18, 
        'xǁConfigTogglerǁtoggle__mutmut_19': xǁConfigTogglerǁtoggle__mutmut_19, 
        'xǁConfigTogglerǁtoggle__mutmut_20': xǁConfigTogglerǁtoggle__mutmut_20, 
        'xǁConfigTogglerǁtoggle__mutmut_21': xǁConfigTogglerǁtoggle__mutmut_21, 
        'xǁConfigTogglerǁtoggle__mutmut_22': xǁConfigTogglerǁtoggle__mutmut_22, 
        'xǁConfigTogglerǁtoggle__mutmut_23': xǁConfigTogglerǁtoggle__mutmut_23, 
        'xǁConfigTogglerǁtoggle__mutmut_24': xǁConfigTogglerǁtoggle__mutmut_24, 
        'xǁConfigTogglerǁtoggle__mutmut_25': xǁConfigTogglerǁtoggle__mutmut_25, 
        'xǁConfigTogglerǁtoggle__mutmut_26': xǁConfigTogglerǁtoggle__mutmut_26, 
        'xǁConfigTogglerǁtoggle__mutmut_27': xǁConfigTogglerǁtoggle__mutmut_27, 
        'xǁConfigTogglerǁtoggle__mutmut_28': xǁConfigTogglerǁtoggle__mutmut_28, 
        'xǁConfigTogglerǁtoggle__mutmut_29': xǁConfigTogglerǁtoggle__mutmut_29, 
        'xǁConfigTogglerǁtoggle__mutmut_30': xǁConfigTogglerǁtoggle__mutmut_30
    }
    xǁConfigTogglerǁtoggle__mutmut_orig.__name__ = 'xǁConfigTogglerǁtoggle'

    def is_configured(self) -> bool:
        """Return True if AMU includes are currently uncommented"""
        return self._state
