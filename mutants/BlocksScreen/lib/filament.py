# Class that represents a filament spool

from typing import Optional
import enum
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


class Filament:
    """Filament spool"""

    class SpoolBaseWeights(enum.Enum):  # XXX This enum will probably be unnecessary
        """Spool base weights"""

        MINI = 750
        BASE = 1000
        BIG = 3000
        JUMBO = 5000

    class SpoolMaterial(enum.Flag):
        """Spool material types"""

        PLASTIC = enum.auto()
        PAPER = enum.auto()
        UNKNOWN = -1

        def __repr__(self) -> str:
            return "<%s.%s>" % (self.__class__.__name__, self._name_)

    def __init__(
        self,
        name: str,
        temperature: int,
        brand: Optional[str] = None,
        spool_type: Optional[SpoolMaterial] = None,
        spool_weight: Optional[float] = None,
    ):
        args = [name, temperature, brand, spool_type, spool_weight]# type: ignore
        kwargs = {}# type: ignore
        return _mutmut_trampoline(object.__getattribute__(self, 'xǁFilamentǁ__init____mutmut_orig'), object.__getattribute__(self, 'xǁFilamentǁ__init____mutmut_mutants'), args, kwargs, self)

    def xǁFilamentǁ__init____mutmut_orig(
        self,
        name: str,
        temperature: int,
        brand: Optional[str] = None,
        spool_type: Optional[SpoolMaterial] = None,
        spool_weight: Optional[float] = None,
    ):
        if not isinstance(name, str) or not isinstance(temperature, int):
            raise TypeError("__init__() invalid argument type")

        self._name: str = name
        self._temperature: int = temperature
        self._weight: Optional[float] = None
        self._brand: Optional[str] = brand

        if spool_type is not None and spool_type in self.SpoolMaterial:
            self._spool_type = spool_type

        self._spool_weight = spool_weight

    def xǁFilamentǁ__init____mutmut_1(
        self,
        name: str,
        temperature: int,
        brand: Optional[str] = None,
        spool_type: Optional[SpoolMaterial] = None,
        spool_weight: Optional[float] = None,
    ):
        if not isinstance(name, str) and not isinstance(temperature, int):
            raise TypeError("__init__() invalid argument type")

        self._name: str = name
        self._temperature: int = temperature
        self._weight: Optional[float] = None
        self._brand: Optional[str] = brand

        if spool_type is not None and spool_type in self.SpoolMaterial:
            self._spool_type = spool_type

        self._spool_weight = spool_weight

    def xǁFilamentǁ__init____mutmut_2(
        self,
        name: str,
        temperature: int,
        brand: Optional[str] = None,
        spool_type: Optional[SpoolMaterial] = None,
        spool_weight: Optional[float] = None,
    ):
        if isinstance(name, str) or not isinstance(temperature, int):
            raise TypeError("__init__() invalid argument type")

        self._name: str = name
        self._temperature: int = temperature
        self._weight: Optional[float] = None
        self._brand: Optional[str] = brand

        if spool_type is not None and spool_type in self.SpoolMaterial:
            self._spool_type = spool_type

        self._spool_weight = spool_weight

    def xǁFilamentǁ__init____mutmut_3(
        self,
        name: str,
        temperature: int,
        brand: Optional[str] = None,
        spool_type: Optional[SpoolMaterial] = None,
        spool_weight: Optional[float] = None,
    ):
        if not isinstance(name, str) or isinstance(temperature, int):
            raise TypeError("__init__() invalid argument type")

        self._name: str = name
        self._temperature: int = temperature
        self._weight: Optional[float] = None
        self._brand: Optional[str] = brand

        if spool_type is not None and spool_type in self.SpoolMaterial:
            self._spool_type = spool_type

        self._spool_weight = spool_weight

    def xǁFilamentǁ__init____mutmut_4(
        self,
        name: str,
        temperature: int,
        brand: Optional[str] = None,
        spool_type: Optional[SpoolMaterial] = None,
        spool_weight: Optional[float] = None,
    ):
        if not isinstance(name, str) or not isinstance(temperature, int):
            raise TypeError(None)

        self._name: str = name
        self._temperature: int = temperature
        self._weight: Optional[float] = None
        self._brand: Optional[str] = brand

        if spool_type is not None and spool_type in self.SpoolMaterial:
            self._spool_type = spool_type

        self._spool_weight = spool_weight

    def xǁFilamentǁ__init____mutmut_5(
        self,
        name: str,
        temperature: int,
        brand: Optional[str] = None,
        spool_type: Optional[SpoolMaterial] = None,
        spool_weight: Optional[float] = None,
    ):
        if not isinstance(name, str) or not isinstance(temperature, int):
            raise TypeError("XX__init__() invalid argument typeXX")

        self._name: str = name
        self._temperature: int = temperature
        self._weight: Optional[float] = None
        self._brand: Optional[str] = brand

        if spool_type is not None and spool_type in self.SpoolMaterial:
            self._spool_type = spool_type

        self._spool_weight = spool_weight

    def xǁFilamentǁ__init____mutmut_6(
        self,
        name: str,
        temperature: int,
        brand: Optional[str] = None,
        spool_type: Optional[SpoolMaterial] = None,
        spool_weight: Optional[float] = None,
    ):
        if not isinstance(name, str) or not isinstance(temperature, int):
            raise TypeError("__INIT__() INVALID ARGUMENT TYPE")

        self._name: str = name
        self._temperature: int = temperature
        self._weight: Optional[float] = None
        self._brand: Optional[str] = brand

        if spool_type is not None and spool_type in self.SpoolMaterial:
            self._spool_type = spool_type

        self._spool_weight = spool_weight

    def xǁFilamentǁ__init____mutmut_7(
        self,
        name: str,
        temperature: int,
        brand: Optional[str] = None,
        spool_type: Optional[SpoolMaterial] = None,
        spool_weight: Optional[float] = None,
    ):
        if not isinstance(name, str) or not isinstance(temperature, int):
            raise TypeError("__init__() invalid argument type")

        self._name: str = None
        self._temperature: int = temperature
        self._weight: Optional[float] = None
        self._brand: Optional[str] = brand

        if spool_type is not None and spool_type in self.SpoolMaterial:
            self._spool_type = spool_type

        self._spool_weight = spool_weight

    def xǁFilamentǁ__init____mutmut_8(
        self,
        name: str,
        temperature: int,
        brand: Optional[str] = None,
        spool_type: Optional[SpoolMaterial] = None,
        spool_weight: Optional[float] = None,
    ):
        if not isinstance(name, str) or not isinstance(temperature, int):
            raise TypeError("__init__() invalid argument type")

        self._name: str = name
        self._temperature: int = None
        self._weight: Optional[float] = None
        self._brand: Optional[str] = brand

        if spool_type is not None and spool_type in self.SpoolMaterial:
            self._spool_type = spool_type

        self._spool_weight = spool_weight

    def xǁFilamentǁ__init____mutmut_9(
        self,
        name: str,
        temperature: int,
        brand: Optional[str] = None,
        spool_type: Optional[SpoolMaterial] = None,
        spool_weight: Optional[float] = None,
    ):
        if not isinstance(name, str) or not isinstance(temperature, int):
            raise TypeError("__init__() invalid argument type")

        self._name: str = name
        self._temperature: int = temperature
        self._weight: Optional[float] = ""
        self._brand: Optional[str] = brand

        if spool_type is not None and spool_type in self.SpoolMaterial:
            self._spool_type = spool_type

        self._spool_weight = spool_weight

    def xǁFilamentǁ__init____mutmut_10(
        self,
        name: str,
        temperature: int,
        brand: Optional[str] = None,
        spool_type: Optional[SpoolMaterial] = None,
        spool_weight: Optional[float] = None,
    ):
        if not isinstance(name, str) or not isinstance(temperature, int):
            raise TypeError("__init__() invalid argument type")

        self._name: str = name
        self._temperature: int = temperature
        self._weight: Optional[float] = None
        self._brand: Optional[str] = None

        if spool_type is not None and spool_type in self.SpoolMaterial:
            self._spool_type = spool_type

        self._spool_weight = spool_weight

    def xǁFilamentǁ__init____mutmut_11(
        self,
        name: str,
        temperature: int,
        brand: Optional[str] = None,
        spool_type: Optional[SpoolMaterial] = None,
        spool_weight: Optional[float] = None,
    ):
        if not isinstance(name, str) or not isinstance(temperature, int):
            raise TypeError("__init__() invalid argument type")

        self._name: str = name
        self._temperature: int = temperature
        self._weight: Optional[float] = None
        self._brand: Optional[str] = brand

        if spool_type is not None or spool_type in self.SpoolMaterial:
            self._spool_type = spool_type

        self._spool_weight = spool_weight

    def xǁFilamentǁ__init____mutmut_12(
        self,
        name: str,
        temperature: int,
        brand: Optional[str] = None,
        spool_type: Optional[SpoolMaterial] = None,
        spool_weight: Optional[float] = None,
    ):
        if not isinstance(name, str) or not isinstance(temperature, int):
            raise TypeError("__init__() invalid argument type")

        self._name: str = name
        self._temperature: int = temperature
        self._weight: Optional[float] = None
        self._brand: Optional[str] = brand

        if spool_type is None and spool_type in self.SpoolMaterial:
            self._spool_type = spool_type

        self._spool_weight = spool_weight

    def xǁFilamentǁ__init____mutmut_13(
        self,
        name: str,
        temperature: int,
        brand: Optional[str] = None,
        spool_type: Optional[SpoolMaterial] = None,
        spool_weight: Optional[float] = None,
    ):
        if not isinstance(name, str) or not isinstance(temperature, int):
            raise TypeError("__init__() invalid argument type")

        self._name: str = name
        self._temperature: int = temperature
        self._weight: Optional[float] = None
        self._brand: Optional[str] = brand

        if spool_type is not None and spool_type not in self.SpoolMaterial:
            self._spool_type = spool_type

        self._spool_weight = spool_weight

    def xǁFilamentǁ__init____mutmut_14(
        self,
        name: str,
        temperature: int,
        brand: Optional[str] = None,
        spool_type: Optional[SpoolMaterial] = None,
        spool_weight: Optional[float] = None,
    ):
        if not isinstance(name, str) or not isinstance(temperature, int):
            raise TypeError("__init__() invalid argument type")

        self._name: str = name
        self._temperature: int = temperature
        self._weight: Optional[float] = None
        self._brand: Optional[str] = brand

        if spool_type is not None and spool_type in self.SpoolMaterial:
            self._spool_type = None

        self._spool_weight = spool_weight

    def xǁFilamentǁ__init____mutmut_15(
        self,
        name: str,
        temperature: int,
        brand: Optional[str] = None,
        spool_type: Optional[SpoolMaterial] = None,
        spool_weight: Optional[float] = None,
    ):
        if not isinstance(name, str) or not isinstance(temperature, int):
            raise TypeError("__init__() invalid argument type")

        self._name: str = name
        self._temperature: int = temperature
        self._weight: Optional[float] = None
        self._brand: Optional[str] = brand

        if spool_type is not None and spool_type in self.SpoolMaterial:
            self._spool_type = spool_type

        self._spool_weight = None
    
    xǁFilamentǁ__init____mutmut_mutants : ClassVar[MutantDict] = { # type: ignore
    'xǁFilamentǁ__init____mutmut_1': xǁFilamentǁ__init____mutmut_1, 
        'xǁFilamentǁ__init____mutmut_2': xǁFilamentǁ__init____mutmut_2, 
        'xǁFilamentǁ__init____mutmut_3': xǁFilamentǁ__init____mutmut_3, 
        'xǁFilamentǁ__init____mutmut_4': xǁFilamentǁ__init____mutmut_4, 
        'xǁFilamentǁ__init____mutmut_5': xǁFilamentǁ__init____mutmut_5, 
        'xǁFilamentǁ__init____mutmut_6': xǁFilamentǁ__init____mutmut_6, 
        'xǁFilamentǁ__init____mutmut_7': xǁFilamentǁ__init____mutmut_7, 
        'xǁFilamentǁ__init____mutmut_8': xǁFilamentǁ__init____mutmut_8, 
        'xǁFilamentǁ__init____mutmut_9': xǁFilamentǁ__init____mutmut_9, 
        'xǁFilamentǁ__init____mutmut_10': xǁFilamentǁ__init____mutmut_10, 
        'xǁFilamentǁ__init____mutmut_11': xǁFilamentǁ__init____mutmut_11, 
        'xǁFilamentǁ__init____mutmut_12': xǁFilamentǁ__init____mutmut_12, 
        'xǁFilamentǁ__init____mutmut_13': xǁFilamentǁ__init____mutmut_13, 
        'xǁFilamentǁ__init____mutmut_14': xǁFilamentǁ__init____mutmut_14, 
        'xǁFilamentǁ__init____mutmut_15': xǁFilamentǁ__init____mutmut_15
    }
    xǁFilamentǁ__init____mutmut_orig.__name__ = 'xǁFilamentǁ__init__'

    @property
    def name(self) -> str:
        return self._name

    @property
    def temperature(self) -> int:
        return self._temperature

    @property
    def weight(self) -> Optional[float]:
        if self._weight is None:
            return
        return self._weight

    @weight.setter
    def weight(self, new_value: float):
        self._weight = new_value

    @property
    def brand(self) -> Optional[str]:
        return self._brand

    @brand.setter
    def brand(self, new_value: str) -> Optional[str]:
        self._brand = new_value

    @property
    def spool_type(self) -> Optional[SpoolMaterial]:
        return self._spool_type

    @spool_type.setter
    def spool_type(self, new):
        if new not in self.SpoolMaterial:
            if isinstance(new, self.SpoolMaterial):
                raise ValueError(
                    "Spool Material type is invalid"
                )  # Correct type but invalid option
        self._spool_type = new
