from typing import Optional


import enum


# typing.Optional[type()] == typing.Union[type(), None]


class Filament:
    class SpoolBaseWeights(enum.Enum):  # XXX This enum will probably be unnecessary
        MINI = 750
        BASE = 1000
        BIG = 3000
        JUMBO = 5000

    class SpoolMaterial(enum.Flag):
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
        if not isinstance(name, str) or not isinstance(temperature, int):
            raise TypeError("__init__() invalid argument type")

        self._name: str = name
        self._temperature: int = temperature
        self._weight: Optional[float] = None
        self._brand: Optional[str] = brand

        if spool_type is not None and spool_type in self.SpoolMaterial:
            self._spool_type = spool_type

        self._spool_weight = spool_weight

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
            else:
                raise TypeError("")  # TODO: Finish this type raise
        self._spool_type = new

    def calc_remaining_weight(self): ...  # TODO calculate remaining spool weight

    def calc_initial_weight(self): ...  # TODO calculate initial spool weight
