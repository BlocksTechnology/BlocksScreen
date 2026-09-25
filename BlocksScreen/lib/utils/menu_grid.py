"""Fixed-height wrapper for the 2-column menu button grids used by the tabs."""

from PyQt6 import QtWidgets

MENU_ROW_H = 80


def fixed_menu_grid(
    parent: QtWidgets.QWidget, grid: QtWidgets.QGridLayout, rows: int = 3
) -> QtWidgets.QWidget:
    """Wrap a menu grid in a fixed-height widget so its rows never shift.

    Args:
        parent: Parent widget of the returned container.
        grid: The button grid to wrap.
        rows: Number of rows to reserve, whether or not they are filled.

    Returns:
        The container widget holding ``grid``.
    """
    for r in range(rows):
        grid.setRowMinimumHeight(r, MENU_ROW_H)
    grid.setContentsMargins(0, 0, 0, 0)
    container = QtWidgets.QWidget(parent)
    container.setLayout(grid)
    container.setSizePolicy(
        QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed
    )
    spacing = max(grid.verticalSpacing(), 0)
    container.setFixedHeight(MENU_ROW_H * rows + spacing * (rows - 1))
    return container
