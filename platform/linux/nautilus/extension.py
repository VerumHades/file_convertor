import os
import subprocess
from urllib.parse import unquote
from typing import List
from gi.repository import Nautilus, GObject

class ImageConverterExtension(GObject.GObject, Nautilus.MenuProvider):
    """Nautilus extension provider that injects a context menu option for image conversion."""

    def _launch_converter_dialog(self, file_path: str) -> None:
        """Launch the standalone image converter graphical user interface as a detached subprocess."""
        script_directory = os.path.dirname(os.path.abspath(__file__))
        converter_executable_path = os.path.join(script_directory, "image_converter_gui.py")
        subprocess.Popen(["python3", converter_executable_path, file_path])

    def _handle_menu_activation(self, menu_item: Nautilus.MenuItem, file_object: Nautilus.FileInfo) -> None:
        """Handle the context menu click event by extracting the local file path and launching the converter."""
        file_uri = file_object.get_uri()
        if file_uri.startswith("file://"):
            file_path = unquote(file_uri[7:])
            self._launch_converter_dialog(file_path)

    def get_file_items(self, files: List[Nautilus.FileInfo]) -> List[Nautilus.MenuItem]:
        """Provide context menu items when specific files are selected in Nautilus."""
        if len(files) != 1:
            return []

        file_object = files[0]
        if file_object.is_directory() or file_object.get_uri_scheme() != "file":
            return []

        file_extension = file_object.get_name().split(".")[-1].lower()
        supported_extensions = {"png", "jpg", "jpeg", "jfif", "webp"}
        if file_extension not in supported_extensions:
            return []

        menu_item = Nautilus.MenuItem(
            name="ImageConverterExtension::ConvertImage",
            label="Convert Image...",
            tip="Convert image format"
        )
        menu_item.connect("activate", self._handle_menu_activation, file_object)
        return [menu_item]