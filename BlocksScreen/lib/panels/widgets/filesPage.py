import json
import logging
import typing

import helper_methods
from lib.utils.blocks_Scrollbar import CustomScrollBar
from lib.utils.icon_button import IconButton
from lib.utils.list_model import EntryDelegate, EntryListModel, ListItem
from PyQt6 import QtCore, QtGui, QtWidgets

logger = logging.getLogger(__name__)


class FilesPage(QtWidgets.QWidget):
    """
    Widget for displaying and navigating gcode files.

    This widget displays a list of gcode files and directories,
    allowing navigation and file selection. It receives updates
    from the Files manager via signals.
    Signals emitted:
    - request_back: User wants to go back (header button)
    - file_selected(str, dict): User selected a file
    - request_file_info(str): Request metadata for a file
    - request_dir_info(str): Request directory contents
    - request_file_metadata(str): Request gcode metadata
    """

    # Signals
    request_back = QtCore.pyqtSignal(name="request_back")
    file_selected = QtCore.pyqtSignal(str, dict, name="file_selected")
    request_file_info = QtCore.pyqtSignal(str, name="request_file_info")
    request_dir_info = QtCore.pyqtSignal(
        [], [str], [str, bool], name="api_get_dir_info"
    )
    request_file_list = QtCore.pyqtSignal([], [str], name="api_get_files_list")
    request_file_metadata = QtCore.pyqtSignal(str, name="api_get_gcode_metadata")
    request_scan_metadata = QtCore.pyqtSignal(str, name="api_scan_gcode_metadata")

    # Constants
    GCODE_EXTENSION = ".gcode"
    USB_PREFIX = "USB-"
    ITEM_HEIGHT = 80
    LEFT_FONT_SIZE = 17
    RIGHT_FONT_SIZE = 12

    # Icon paths
    ICON_PATHS = {
        "back_folder": ":/ui/media/btn_icons/back_folder.svg",
        "folder": ":/ui/media/btn_icons/folderIcon.svg",
        "right_arrow": ":/arrow_icons/media/btn_icons/right_arrow.svg",
        "usb": ":/ui/media/btn_icons/usb_icon.svg",
        "back": ":/ui/media/btn_icons/back.svg",
        "refresh": ":/ui/media/btn_icons/refresh.svg",
    }

    def __init__(self, parent: typing.Optional[QtWidgets.QWidget] = None) -> None:
        super().__init__(parent)

        self._file_list: list[dict] = []
        self._files_data: dict[str, dict] = {}  # filename -> metadata dict
        self._directories: list[dict] = []
        self._curr_dir: str = ""
        self._pending_action: bool = False
        self._pending_metadata_requests: set[str] = set()  # Track pending requests
        self._metadata_retry_count: dict[
            str, int
        ] = {}  # Track retry count per file (max 3)
        self._icons: dict[str, QtGui.QPixmap] = {}

        self._model = EntryListModel()
        self._entry_delegate = EntryDelegate()

        self._setup_ui()
        self._load_icons()
        self._connect_signals()

        self.setMouseTracking(True)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_AcceptTouchEvents, True)

    @property
    def current_directory(self) -> str:
        """Get current directory path."""
        return self._curr_dir

    @current_directory.setter
    def current_directory(self, value: str) -> None:
        """Set current directory path."""
        self._curr_dir = value

    def reload_gcodes_folder(self) -> None:
        """Request reload of the gcodes folder from root."""
        logger.debug("Reloading gcodes folder")
        self.request_dir_info[str].emit("")

    def clear_files_data(self) -> None:
        """Clear all cached file data."""
        self._files_data.clear()
        self._pending_metadata_requests.clear()
        self._metadata_retry_count.clear()

    def retry_metadata_request(self, file_path: str) -> bool:
        """
        Request metadata with a maximum of 3 retries per file.
        Args:
            file_path: Path to the file
        Returns:
            True if request was made, False if max retries reached
        """
        clean_path = file_path.removeprefix("/")

        if not clean_path.lower().endswith(self.GCODE_EXTENSION):
            return False

        current_count = self._metadata_retry_count.get(clean_path, 0)

        if current_count > 3:
            # Maximum 3 force scan per file
            logger.debug(f"Metadata retry limit reached for: {clean_path}")
            return False

        self._metadata_retry_count[clean_path] = current_count + 1

        if current_count == 0:
            # First attempt: regular metadata request
            self.request_file_metadata.emit(clean_path)
            logger.debug(f"Metadata request 1/3 for: {clean_path}")
        else:
            # Second and third attempts: force scan
            self.request_scan_metadata.emit(clean_path)
            logger.debug(f"Metadata scan {current_count + 1}/3 for: {clean_path}")

        return True

    @QtCore.pyqtSlot(list, name="on_file_list")
    def on_file_list(self, file_list: list) -> None:
        """Handle receiving full files list."""
        self._file_list = file_list.copy() if file_list else []
        logger.debug(f"Received file list with {len(self._file_list)} files")

    @QtCore.pyqtSlot(list, name="on_dirs")
    def on_directories(self, directories_data: list) -> None:
        """Handle receiving full directories list."""
        self._directories = directories_data.copy() if directories_data else []
        logger.debug(f"Received {len(self._directories)} directories")

        if self.isVisible():
            self._build_file_list()

    @QtCore.pyqtSlot(dict, name="on_fileinfo")
    def on_fileinfo(self, filedata: dict) -> None:
        """
        Handle receiving file metadata.

        Updates existing file entry in the list with better info (time, filament).
        """
        if not filedata or not self.isVisible():
            return

        filename = filedata.get("filename", "")
        if not filename or not filename.lower().endswith(self.GCODE_EXTENSION):
            return

        # Cache the file data
        self._files_data[filename] = filedata

        # Remove from pending requests and reset retry count (success)
        self._pending_metadata_requests.discard(filename)
        self._metadata_retry_count.pop(filename, None)

        # Check if this file should be displayed in current view
        file_dir = self._get_parent_directory(filename)
        current = self._curr_dir.removeprefix("/")

        # Both empty = root directory, otherwise must match exactly
        if file_dir != current:
            return

        display_name = self._get_display_name(filename)
        item = self._create_file_list_item(filedata)
        if not item:
            return

        self._model.remove_item_by_text(display_name)

        # Find correct position (sorted by modification time, newest first)
        insert_position = self._find_file_insert_position(filedata.get("modified", 0))
        self._model.insert_item(insert_position, item)

        logger.debug(f"Updated file in list: {display_name}")

    @QtCore.pyqtSlot(str, name="on_metadata_error")
    def on_metadata_error(self, filename: str) -> None:
        """
        Handle metadata request failure.

        Triggers retry with scan_gcode_metadata if under retry limit.
        Called when metadata request fails.
        """
        if not filename:
            return

        clean_filename = filename.removeprefix("/")

        if clean_filename not in self._pending_metadata_requests:
            return

        # Try again (will use force scan to the max  of 3 times)
        if not self.retry_metadata_request(clean_filename):
            # Max retries reached, remove from pending
            self._pending_metadata_requests.discard(clean_filename)
            logger.debug(f"Giving up on metadata for: {clean_filename}")

    @QtCore.pyqtSlot(str, list, name="on_usb_files_loaded")
    def on_usb_files_loaded(self, usb_path: str, files: list) -> None:
        """
        Handle preloaded USB files.

        Called when USB files are preloaded in background.
        If we're currently viewing this USB, update the display.

        Args:
            usb_path: The USB mount path
            files: List of file dicts from the USB
        """
        current = self._curr_dir.removeprefix("/")

        # If we're currently in this USB folder, update the file list
        if current == usb_path:
            self._file_list = files.copy()
            if self.isVisible():
                self._build_file_list()
            logger.debug(f"Updated view with preloaded USB files: {usb_path}")

    def _find_file_insert_position(self, modified_time: float) -> int:
        """
        Find the correct position to insert a new file.

        Files should be:
        1. After all directories
        2. Sorted by modification time (newest first)

        Returns:
            The index at which to insert the new file.
        """
        insert_pos = 0

        for i in range(self._model.rowCount()):
            index = self._model.index(i)
            item = self._model.data(index, QtCore.Qt.ItemDataRole.UserRole)

            if not item:
                continue

            # Skip directories (items with left_icon)
            if item.left_icon:
                insert_pos = i + 1
                continue

            # This is a file - check its modification time
            file_key = self._find_file_key_by_display_name(item.text)
            if file_key:
                file_data = self._files_data.get(file_key, {})
                file_modified = file_data.get("modified", 0)

                # Files are sorted newest first, so insert before older files
                if modified_time > file_modified:
                    return i

            insert_pos = i + 1

        return insert_pos

    def _find_file_key_by_display_name(self, display_name: str) -> typing.Optional[str]:
        """Find the file key in _files_data by its display name."""
        for key in self._files_data:
            if self._get_display_name(key) == display_name:
                return key
        return None

    @QtCore.pyqtSlot(dict, name="on_file_added")
    def on_file_added(self, file_data: dict) -> None:
        """
        Handle a single file being added.

        Called when Moonraker sends notify_filelist_changed with create_file action.
        Adds file to list immediately, metadata updates later.
        """
        path = file_data.get("path", file_data.get("filename", ""))
        if not path:
            return

        # Normalize paths
        path = path.removeprefix("/")
        file_dir = self._get_parent_directory(path)
        current = self._curr_dir.removeprefix("/")

        # Check if file belongs to current directory
        if file_dir != current:
            logger.debug(
                f"File '{path}' (dir: '{file_dir}') not in current directory ('{current}'), skipping"
            )
            return

        # Only update UI if visible
        if not self.isVisible():
            logger.debug("Widget not visible, will refresh on show")
            return

        display_name = self._get_display_name(path)

        if not self._model_contains_item(display_name):
            # Create basic item with unknown info
            modified = file_data.get("modified", 0)

            item = ListItem(
                text=display_name,
                right_text="Unknown Filament - Unknown time",
                right_icon=self._icons.get("right_arrow"),
                left_icon=None,
                callback=None,
                selected=False,
                allow_check=False,
                _lfontsize=self.LEFT_FONT_SIZE,
                _rfontsize=self.RIGHT_FONT_SIZE,
                height=self.ITEM_HEIGHT,
                notificate=False,
            )

            # Find correct position
            insert_position = self._find_file_insert_position(modified)
            self._model.insert_item(insert_position, item)
            self._setup_scrollbar()
            self._hide_placeholder()
            logger.debug(f"Added new file to list: {display_name}")

        # Request metadata for gcode files using retry mechanism
        if path.lower().endswith(self.GCODE_EXTENSION):
            if path not in self._pending_metadata_requests:
                self._pending_metadata_requests.add(path)
                self.retry_metadata_request(path)
                logger.debug(f"Requested metadata for new file: {path}")

    @QtCore.pyqtSlot(str, name="on_file_removed")
    def on_file_removed(self, filepath: str) -> None:
        """
        Handle a file being removed.

        Called when Moonraker sends notify_filelist_changed with delete_file action.
        """
        filepath = filepath.removeprefix("/")
        file_dir = self._get_parent_directory(filepath)
        current = self._curr_dir.removeprefix("/")

        # Always clean up cache
        self._files_data.pop(filepath, None)
        self._pending_metadata_requests.discard(filepath)
        self._metadata_retry_count.pop(filepath, None)

        # Only update UI if visible and in current directory
        if not self.isVisible():
            return

        if file_dir != current:
            logger.debug(
                f"Deleted file '{filepath}' not in current directory ('{current}'), skipping UI update"
            )
            return

        filename = self._get_basename(filepath)
        display_name = self._get_display_name(filename)

        # Remove from model
        removed = self._model.remove_item_by_text(display_name)

        if removed:
            self._setup_scrollbar()
            self._check_empty_state()
            logger.debug(f"File removed from view: {filepath}")

    @QtCore.pyqtSlot(dict, name="on_file_modified")
    def on_file_modified(self, file_data: dict) -> None:
        """
        Handle a file being modified.

        Called when Moonraker sends notify_filelist_changed with modify_file action.
        """
        path = file_data.get("path", file_data.get("filename", ""))
        if path:
            # Remove old entry and request fresh metadata
            self.on_file_removed(path)
            self.on_file_added(file_data)

    @QtCore.pyqtSlot(dict, name="on_dir_added")
    def on_dir_added(self, dir_data: dict) -> None:
        """
        Handle a directory being added.

        Called when Moonraker sends notify_filelist_changed with create_dir action.
        Inserts the directory in the correct sorted position (alphabetically, after Go Back).
        """
        # Extract dirname from path or dirname field
        path = dir_data.get("path", "")
        dirname = dir_data.get("dirname", "")

        if not dirname and path:
            dirname = self._get_basename(path)

        if not dirname or dirname.startswith("."):
            return

        path = path.removeprefix("/")
        parent_dir = self._get_parent_directory(path) if path else ""
        current = self._curr_dir.removeprefix("/")

        if parent_dir != current:
            logger.debug(
                f"Directory '{dirname}' (parent: '{parent_dir}') not in current directory ('{current}'), skipping"
            )
            return

        if not self.isVisible():
            logger.debug(
                f"Widget not visible, skipping UI update for added dir: {dirname}"
            )
            return

        # Check if already exists
        if self._model_contains_item(dirname):
            return

        # Ensure dirname is in dir_data
        dir_data["dirname"] = dirname

        # Find the correct sorted position for this directory
        insert_position = self._find_directory_insert_position(dirname)

        # Create the list item
        icon = self._icons.get("folder")
        if self._is_usb_directory(self._curr_dir, dirname):
            icon = self._icons.get("usb")

        item = ListItem(
            text=str(dirname),
            left_icon=icon,
            right_text="",
            right_icon=None,
            selected=False,
            callback=None,
            allow_check=False,
            _lfontsize=self.LEFT_FONT_SIZE,
            _rfontsize=self.RIGHT_FONT_SIZE,
            height=self.ITEM_HEIGHT,
        )

        # Insert at the correct position
        self._model.insert_item(insert_position, item)

        self._setup_scrollbar()
        self._hide_placeholder()
        logger.debug(
            f"Directory added to view at position {insert_position}: {dirname}"
        )

    def _find_directory_insert_position(self, new_dirname: str) -> int:
        """
        Find the correct position to insert a new directory.

        Directories should be:
        1. After "Go Back" (if present)
        2. Before all files
        3. Sorted alphabetically among other directories

        Returns:
            The index at which to insert the new directory.
        """
        new_dirname_lower = new_dirname.lower()
        insert_pos = 0

        for i in range(self._model.rowCount()):
            index = self._model.index(i)
            item = self._model.data(index, QtCore.Qt.ItemDataRole.UserRole)

            if not item:
                continue

            # Skip "Go Back" - always stays at top
            if item.text == "Go Back":
                insert_pos = i + 1
                continue

            # If this item has a left_icon, it's a directory
            if item.left_icon:
                # Compare alphabetically
                if item.text.lower() > new_dirname_lower:
                    # Found a directory that should come after the new one
                    return i
                else:
                    # This directory comes before, keep looking
                    insert_pos = i + 1
            else:
                # Hit a file - insert before it (directories come before files)
                return i

        # Insert at the end of directories (or end of list if no files)
        return insert_pos

    @QtCore.pyqtSlot(str, name="on_dir_removed")
    def on_dir_removed(self, dirname_or_path: str) -> None:
        """
        Handle a directory being removed.

        Called when Moonraker sends notify_filelist_changed with delete_dir action.
        Also handles USB mount removal (which Moonraker reports as delete_file).
        """
        dirname_or_path = dirname_or_path.removeprefix("/")
        dirname = (
            self._get_basename(dirname_or_path)
            if "/" in dirname_or_path
            else dirname_or_path
        )

        if not dirname:
            return

        # Check if user is currently inside the removed directory (e.g., USB removed)
        current = self._curr_dir.removeprefix("/")
        if current == dirname or current.startswith(dirname + "/"):
            logger.warning(
                f"Current directory '{current}' was removed, returning to root"
            )
            self.on_directory_error()
            return

        # Skip UI update if not visible
        if not self.isVisible():
            return

        removed = self._model.remove_item_by_text(dirname)

        if removed:
            self._setup_scrollbar()
            self._check_empty_state()
            logger.debug(f"Directory removed from view: {dirname}")

    @QtCore.pyqtSlot(name="on_full_refresh_needed")
    def on_full_refresh_needed(self) -> None:
        """
        Handle full refresh request.

        Called when Moonraker sends root_update or when major changes occur.
        """
        logger.info("Full refresh requested")
        self._curr_dir = ""
        self.request_dir_info[str].emit(self._curr_dir)

    @QtCore.pyqtSlot(name="on_directory_error")
    def on_directory_error(self) -> None:
        """
        Handle Directory Error.

        Immediately navigates back to root gcodes folder.
        Call this from MainWindow when detecting USB removal or directory errors.
        """
        logger.info("Directory Error - returning to root directory")

        # Reset to root directory
        self._curr_dir = ""

        # Clear any pending actions
        self._pending_action = False
        self._pending_metadata_requests.clear()

        # Request fresh data for root directory
        self.request_dir_info[str].emit("")

    @QtCore.pyqtSlot(ListItem, name="on_item_selected")
    def _on_item_selected(self, item: ListItem) -> None:
        """Handle list item selection."""
        if not item.left_icon:
            # File selected (files don't have left icon)
            filename = self._build_filepath(item.text + self.GCODE_EXTENSION)
            self._on_file_item_clicked(filename)
        elif item.text == "Go Back":
            # Go back selected
            go_back_path = self._get_parent_directory(self._curr_dir)
            if go_back_path == "/":
                go_back_path = ""
            self._on_go_back_dir(go_back_path)
        else:
            # Directory selected
            self._on_dir_item_clicked("/" + item.text)

    @QtCore.pyqtSlot(name="reset_dir")
    def reset_dir(self) -> None:
        """Reset to root directory."""
        self._curr_dir = ""
        self.request_dir_info[str].emit(self._curr_dir)

    def showEvent(self, event: QtGui.QShowEvent) -> None:
        """Handle widget becoming visible."""
        # Request fresh data when becoming visible
        self.request_dir_info[str].emit(self._curr_dir)
        super().showEvent(event)

    def hideEvent(self, event: QtGui.QHideEvent) -> None:
        """Handle widget being hidden."""
        # Clear pending requests when hidden
        self._pending_metadata_requests.clear()
        super().hideEvent(event)

    def _build_file_list(self) -> None:
        """Build the complete file list display."""
        self._list_widget.blockSignals(True)
        self._model.clear()
        self._entry_delegate.clear()
        self._pending_action = False
        self._pending_metadata_requests.clear()
        self._metadata_retry_count.clear()

        # Determine if we're in root directory
        is_root = not self._curr_dir or self._curr_dir == "/"

        # Check for empty state in root directory
        if not self._file_list and not self._directories and is_root:
            self._show_placeholder()
            self._list_widget.blockSignals(False)
            return

        # We have content (or we're in a subdirectory), hide placeholder
        self._hide_placeholder()

        # Add back button if not in root
        if not is_root:
            self._add_back_folder_entry()

        # Add directories (sorted alphabetically)
        sorted_dirs = sorted(
            self._directories, key=lambda x: x.get("dirname", "").lower()
        )
        for dir_data in sorted_dirs:
            dirname = dir_data.get("dirname", "")
            if dirname and not dirname.startswith("."):
                self._add_directory_list_item(dir_data)

        # Add files immediately (sorted by modification time, newest first)
        sorted_files = sorted(
            self._file_list, key=lambda x: x.get("modified", 0), reverse=True
        )
        for file_item in sorted_files:
            filename = file_item.get("filename", file_item.get("path", ""))
            if not filename:
                continue

            # Add file to list immediately with basic info
            self._add_file_to_list(file_item)

            # Request metadata for gcode files (will update display later)
            if filename.lower().endswith(self.GCODE_EXTENSION):
                self._request_file_info(file_item)

        self._setup_scrollbar()
        self._list_widget.blockSignals(False)
        self._list_widget.update()

    def _add_file_to_list(self, file_item: dict) -> None:
        """Add a file entry to the list with basic info."""
        filename = file_item.get("filename", file_item.get("path", ""))
        if not filename or not filename.lower().endswith(self.GCODE_EXTENSION):
            return

        # Get display name
        display_name = self._get_display_name(filename)

        # Check if already in list
        if self._model_contains_item(display_name):
            return

        # Use cached metadata if available, otherwise show unknown
        full_path = self._build_filepath(filename)
        cached = self._files_data.get(full_path)

        if cached:
            item = self._create_file_list_item(cached)
        else:
            item = ListItem(
                text=display_name,
                right_text="Unknown Filament - Unknown time",
                right_icon=self._icons.get("right_arrow"),
                left_icon=None,
                callback=None,
                selected=False,
                allow_check=False,
                _lfontsize=self.LEFT_FONT_SIZE,
                _rfontsize=self.RIGHT_FONT_SIZE,
                height=self.ITEM_HEIGHT,
                notificate=False,
            )

        if item:
            self._model.add_item(item)

        self._setup_scrollbar()
        self._list_widget.blockSignals(False)
        self._list_widget.update()

    def _create_file_list_item(self, filedata: dict) -> typing.Optional[ListItem]:
        """Create a ListItem from file metadata."""
        filename = filedata.get("filename", "")
        if not filename:
            return None

        # Format estimated time
        estimated_time = filedata.get("estimated_time", 0)
        seconds = int(estimated_time) if isinstance(estimated_time, (int, float)) else 0
        time_str = self._format_print_time(seconds)

        # Get filament type
        filament_type = filedata.get("filament_type")
        if isinstance(filament_type, str):
            text = filament_type.strip()
            if text.startswith("[") and text.endswith("]"):
                try:
                    types = json.loads(text)
                except json.JSONDecodeError:
                    types = [text]
            else:
                types = [text]
        else:
            types = filament_type or []

        if not isinstance(types, list):
            types = [types]

        filament_type = ",".join(dict.fromkeys(types))

        if not filament_type or filament_type == -1.0 or filament_type == "Unknown":
            filament_type = "Unknown Filament"

        display_name = self._get_display_name(filename)

        return ListItem(
            text=display_name,
            right_text=f"{filament_type} - {time_str}",
            right_icon=self._icons.get("right_arrow"),
            left_icon=None,  # Files have no left icon
            callback=None,
            selected=False,
            allow_check=False,
            _lfontsize=self.LEFT_FONT_SIZE,
            _rfontsize=self.RIGHT_FONT_SIZE,
            height=self.ITEM_HEIGHT,
            notificate=False,
        )

    def _add_directory_list_item(self, dir_data: dict) -> None:
        """Add a directory entry to the list."""
        dir_name = dir_data.get("dirname", "")
        if not dir_name:
            return

        # Choose appropriate icon
        icon = self._icons.get("folder")
        if self._is_usb_directory(self._curr_dir, dir_name):
            icon = self._icons.get("usb")

        item = ListItem(
            text=str(dir_name),
            left_icon=icon,
            right_text="",
            right_icon=None,
            selected=False,
            callback=None,
            allow_check=False,
            _lfontsize=self.LEFT_FONT_SIZE,
            _rfontsize=self.RIGHT_FONT_SIZE,
            height=self.ITEM_HEIGHT,
        )
        self._model.add_item(item)

    def _add_back_folder_entry(self) -> None:
        """Add the 'Go Back' navigation entry."""
        item = ListItem(
            text="Go Back",
            right_text="",
            right_icon=None,
            left_icon=self._icons.get("back_folder"),
            callback=None,
            selected=False,
            allow_check=False,
            _lfontsize=self.LEFT_FONT_SIZE,
            _rfontsize=self.RIGHT_FONT_SIZE,
            height=self.ITEM_HEIGHT,
            notificate=False,
        )
        self._model.add_item(item)

    def _request_file_info(self, file_data_item: dict) -> None:
        """Request metadata for a file item using retry mechanism."""
        if not file_data_item:
            return

        name = file_data_item.get("path", file_data_item.get("filename", ""))
        if not name or not name.lower().endswith(self.GCODE_EXTENSION):
            return

        # Build full path
        file_path = self._build_filepath(name)

        # Track pending request
        self._pending_metadata_requests.add(file_path)

        # Use retry mechanism (first attempt uses get_gcode_metadata)
        self.retry_metadata_request(file_path)

    def _on_file_item_clicked(self, filename: str) -> None:
        """Handle file item click."""
        clean_filename = filename.removeprefix("/")
        file_data = self._files_data.get(clean_filename, {})
        self.file_selected.emit(clean_filename, file_data)

    def _on_dir_item_clicked(self, directory: str) -> None:
        """Handle directory item click."""
        if self._pending_action:
            return

        self._curr_dir = self._curr_dir + directory
        self.request_dir_info[str].emit(self._curr_dir)
        self._pending_action = True

    def _on_go_back_dir(self, directory: str) -> None:
        """Handle go back navigation."""
        self.request_dir_info[str].emit(directory)
        self._curr_dir = directory

    def _show_placeholder(self) -> None:
        """Show the 'No Files found' placeholder."""
        self._scrollbar.hide()
        self._list_widget.hide()
        self._label.show()

    def _hide_placeholder(self) -> None:
        """Hide the placeholder and show the list."""
        self._label.hide()
        self._list_widget.show()
        self._scrollbar.show()

    def _check_empty_state(self) -> None:
        """Check if list is empty and show placeholder if needed."""
        is_root = not self._curr_dir or self._curr_dir == "/"

        if self._model.rowCount() == 0 and is_root:
            self._show_placeholder()
        elif self._model.rowCount() == 0 and not is_root:
            # In subdirectory with no files - just show "Go Back"
            self._add_back_folder_entry()

    def _model_contains_item(self, text: str) -> bool:
        """Check if model contains an item with the given text."""
        for i in range(self._model.rowCount()):
            index = self._model.index(i)
            item = self._model.data(index, QtCore.Qt.ItemDataRole.UserRole)
            if item and item.text == text:
                return True
        return False

    def _handle_scrollbar_value_changed(self, value: int) -> None:
        """Sync scrollbar with list widget."""
        self._scrollbar.blockSignals(True)
        self._scrollbar.setValue(value)
        self._scrollbar.blockSignals(False)

    def _setup_scrollbar(self) -> None:
        """Configure scrollbar to match list size."""
        list_scrollbar = self._list_widget.verticalScrollBar()
        self._scrollbar.setMinimum(list_scrollbar.minimum())
        self._scrollbar.setMaximum(list_scrollbar.maximum())
        self._scrollbar.setPageStep(list_scrollbar.pageStep())

        if list_scrollbar.maximum() > 0:
            self._scrollbar.show()
        else:
            self._scrollbar.hide()

    @staticmethod
    def _get_basename(path: str) -> str:
        """
        Get the basename of a path without using os.path.
        Works with paths from Moonraker (forward slashes only).
        """
        if not path:
            return ""
        # Remove trailing slashes and get last component
        path = path.rstrip("/")
        if "/" in path:
            return path.rsplit("/", 1)[-1]
        return path

    @staticmethod
    def _get_parent_directory(path: str) -> str:
        """
        Get the parent directory of a path without using os.path.
        Works with paths from Moonraker (forward slashes only).
        """
        if not path:
            return ""
        path = path.removeprefix("/").rstrip("/")
        if "/" in path:
            return path.rsplit("/", 1)[0]
        return ""

    def _build_filepath(self, filename: str) -> str:
        """Build full file path from current directory and filename."""
        filename = filename.removeprefix("/")
        if self._curr_dir:
            curr = self._curr_dir.removeprefix("/")
            return f"{curr}/{filename}"
        return filename

    @staticmethod
    def _is_usb_directory(parent_dir: str, directory_name: str) -> bool:
        """Check if directory is a USB mount in the root."""
        return parent_dir == "" and directory_name.startswith("USB-")

    @staticmethod
    def _format_print_time(seconds: int) -> str:
        """Format print time in human-readable form."""
        if seconds <= 0:
            return "Unknown time"
        if seconds < 60:
            return f"{seconds}m"

        days, hours, minutes, _ = helper_methods.estimate_print_time(seconds)

        if days > 0:
            return f"{days}d {hours}h {minutes}m"
        elif hours > 0:
            return f"{hours}h {minutes}m"
        else:
            return f"{minutes}m"

    def _get_display_name(self, filename: str) -> str:
        """Get display name from filename (without path and extension)."""
        basename = self._get_basename(filename)
        name = helper_methods.get_file_name(basename)

        # Remove .gcode extension
        if name.lower().endswith(self.GCODE_EXTENSION):
            name = name[:-6]

        return name

    def _load_icons(self) -> None:
        """Load all icons into cache."""
        self._icons = {
            "back_folder": QtGui.QPixmap(self.ICON_PATHS["back_folder"]),
            "folder": QtGui.QPixmap(self.ICON_PATHS["folder"]),
            "right_arrow": QtGui.QPixmap(self.ICON_PATHS["right_arrow"]),
            "usb": QtGui.QPixmap(self.ICON_PATHS["usb"]),
        }

    def _connect_signals(self) -> None:
        """Connect internal signals."""
        # Button connections
        self._reload_button.clicked.connect(
            lambda: self.request_dir_info[str].emit(self._curr_dir)
        )
        self.back_btn.clicked.connect(self.reset_dir)

        # List widget connections
        self._list_widget.verticalScrollBar().valueChanged.connect(
            self._handle_scrollbar_value_changed
        )
        self._scrollbar.valueChanged.connect(self._handle_scrollbar_value_changed)
        self._scrollbar.valueChanged.connect(
            lambda value: self._list_widget.verticalScrollBar().setValue(value)
        )

        # Delegate connections
        self._entry_delegate.item_selected.connect(self._on_item_selected)

    def _setup_ui(self) -> None:
        """Set up the widget UI."""
        # Size policy
        size_policy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(1)
        self.setSizePolicy(size_policy)
        self.setMinimumSize(QtCore.QSize(710, 400))

        # Font
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.StyleStrategy.PreferAntialias)
        self.setFont(font)

        # Layout direction and style
        self.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.setAutoFillBackground(False)
        self.setStyleSheet("#file_page { background-color: transparent; }")

        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setObjectName("main_layout")

        # Header layout
        header_layout = self._create_header_layout()
        main_layout.addLayout(header_layout)

        # Separator line
        line = QtWidgets.QFrame(parent=self)
        line.setFrameShape(QtWidgets.QFrame.Shape.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        main_layout.addWidget(line)

        # Content layout
        content_layout = self._create_content_layout()
        main_layout.addLayout(content_layout)

    def _create_header_layout(self) -> QtWidgets.QHBoxLayout:
        """Create the header with back and reload buttons."""
        layout = QtWidgets.QHBoxLayout()
        layout.setObjectName("header_layout")

        # Back button
        self.back_btn = IconButton(parent=self)
        self.back_btn.setMinimumSize(QtCore.QSize(60, 60))
        self.back_btn.setMaximumSize(QtCore.QSize(60, 60))
        self.back_btn.setFlat(True)
        self.back_btn.setProperty("icon_pixmap", QtGui.QPixmap(self.ICON_PATHS["back"]))
        self.back_btn.setObjectName("back_btn")
        layout.addWidget(self.back_btn, 0, QtCore.Qt.AlignmentFlag.AlignLeft)

        # Reload button
        self._reload_button = IconButton(parent=self)
        self._reload_button.setMinimumSize(QtCore.QSize(60, 60))
        self._reload_button.setMaximumSize(QtCore.QSize(60, 60))
        self._reload_button.setFlat(True)
        self._reload_button.setProperty(
            "icon_pixmap", QtGui.QPixmap(self.ICON_PATHS["refresh"])
        )
        self._reload_button.setObjectName("reload_button")
        layout.addWidget(self._reload_button, 0, QtCore.Qt.AlignmentFlag.AlignRight)

        return layout

    def _create_content_layout(self) -> QtWidgets.QHBoxLayout:
        """Create the content area with list and scrollbar."""
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setObjectName("content_layout")

        # Placeholder label
        font = QtGui.QFont()
        font.setPointSize(25)
        self._label = QtWidgets.QLabel("No Files found")
        self._label.setFont(font)
        self._label.setStyleSheet("color: gray;")
        self._label.hide()

        # List widget
        self._list_widget = self._create_list_widget()

        # Scrollbar
        self._scrollbar = CustomScrollBar()
        self._scrollbar.show()

        # Add widgets to layout
        layout.addWidget(
            self._label,
            alignment=(
                QtCore.Qt.AlignmentFlag.AlignHCenter
                | QtCore.Qt.AlignmentFlag.AlignVCenter
            ),
        )
        layout.addWidget(self._list_widget)
        layout.addWidget(self._scrollbar)

        return layout

    def _create_list_widget(self) -> QtWidgets.QListView:
        """Create and configure the list view widget."""
        list_widget = QtWidgets.QListView(parent=self)
        list_widget.setModel(self._model)
        list_widget.setItemDelegate(self._entry_delegate)
        list_widget.setSpacing(5)
        list_widget.setProperty("showDropIndicator", False)
        list_widget.setProperty("selectionMode", "NoSelection")
        list_widget.setStyleSheet("background: transparent;")
        list_widget.setDefaultDropAction(QtCore.Qt.DropAction.IgnoreAction)
        list_widget.setUniformItemSizes(True)
        list_widget.setObjectName("list_widget")
        list_widget.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        list_widget.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectionBehavior.SelectItems
        )
        list_widget.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        list_widget.setVerticalScrollMode(
            QtWidgets.QAbstractItemView.ScrollMode.ScrollPerPixel
        )
        list_widget.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        list_widget.setEditTriggers(
            QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers
        )

        # Enable touch gestures
        QtWidgets.QScroller.grabGesture(
            list_widget,
            QtWidgets.QScroller.ScrollerGestureType.TouchGesture,
        )
        QtWidgets.QScroller.grabGesture(
            list_widget,
            QtWidgets.QScroller.ScrollerGestureType.LeftMouseButtonGesture,
        )

        # Configure scroller properties
        scroller = QtWidgets.QScroller.scroller(list_widget)
        props = scroller.scrollerProperties()
        props.setScrollMetric(
            QtWidgets.QScrollerProperties.ScrollMetric.DragVelocitySmoothingFactor,
            0.05,
        )
        props.setScrollMetric(
            QtWidgets.QScrollerProperties.ScrollMetric.DecelerationFactor,
            0.4,
        )
        scroller.setScrollerProperties(props)

        return list_widget
