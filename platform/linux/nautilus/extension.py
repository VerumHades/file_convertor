import os
import subprocess
from urllib.parse import unquote
from typing import List
from gi.repository import Nautilus, GObject

GUI_SCRIPT_PATH = os.path.expanduser("~/.local/share/file-convertor/image_converter_gui.py")

class ImageConverterExtension(GObject.GObject, Nautilus.MenuProvider):
    """Nautilus extension provider that injects a context menu option for batch image conversion."""

    def _launch_converter_dialog(self, file_paths: List[str]) -> None:
        """Launch the standalone image converter graphical user interface with multiple file paths as arguments."""
        subprocess.Popen(["python3", GUI_SCRIPT_PATH] + file_paths)

    def _handle_menu_activation(self, menu_item: Nautilus.MenuItem, file_objects: List[Nautilus.FileInfo]) -> None:
        """Handle the context menu click event by extracting local file paths and launching the batch converter."""
        file_paths = []
        for file_object in file_objects:
            file_uri = file_object.get_uri()
            if file_uri.startswith("file://") and not file_object.is_directory():
                file_paths.append(unquote(file_uri[7:]))
        
        if file_paths:
            self._launch_converter_dialog(file_paths)

    def get_file_items(self, files: List[Nautilus.FileInfo]) -> List[Nautilus.MenuItem]:
        """Provide context menu items when one or more files are selected in Nautilus."""
        if not files:
            return []

        has_valid_file = any(
            not file_object.is_directory() and file_object.get_uri_scheme() == "file"
            for file_object in files
        )

        if not has_valid_file:
            return []

        menu_item = Nautilus.MenuItem(
            name="ImageConverterExtension::BatchConvertImages",
            label="Convert Images...",
            tip="Convert image formats in batch"
        )
        menu_item.connect("activate", self._handle_menu_activation, files)
        return [menu_item]