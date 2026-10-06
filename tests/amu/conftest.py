# Verbatim RF50-Klipper/printer.cfg:155-165, stray pre-bracket space included.
_BANNER = "#" * 94


def _banner(title: str) -> str:
    """Rebuild the 94-char banner byte-exactly; as a literal it would breach E501."""
    return (
        f"{'#' * 47}   {'#' * 44}\n"
        f"{'#' * 39}{title}{'#' * 37}\n"
        f"{'#' * 46}   {'#' * 45}\n"
    )


_AMU_BANNER = _banner("     Amu System   ")
_SINGLE_BANNER = _banner(" Normal system    ")

# AMU off (shipped state): the single-filament include is active.
COMMENTED_CFG = (
    f"{_AMU_BANNER}{_BANNER}\n"
    "#[include config/variant_mmu/base/*.cfg]\n"
    f"{_BANNER}\n"
    f"{_SINGLE_BANNER}{_BANNER}\n"
    "[include config/variant_sync_single/*.cfg ]\n"
    f"{_BANNER}\n"
)

# AMU on: the AMU include is active, the single-filament one commented.
UNCOMMENTED_CFG = (
    f"{_AMU_BANNER}{_BANNER}\n"
    "[include config/variant_mmu/base/*.cfg]\n"
    f"{_BANNER}\n"
    f"{_SINGLE_BANNER}{_BANNER}\n"
    "#[include config/variant_sync_single/*.cfg ]\n"
    f"{_BANNER}\n"
)
