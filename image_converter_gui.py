import sys
import tkinter
from tkinter import ttk
from PIL import Image

file_path = sys.argv[1]

def get_available_target_formats(source_format):
    supported_formats = ["PNG", "JPG", "JPEG", "JFIF", "WEBP"]
    return [format_name for format_name in supported_formats if format_name.lower() != source_format.lower()]

def convert(source_filepath, target_format):
    base_path, _ = source_filepath.rsplit(".", 1)
    target_filepath = f"{base_path}.{target_format.lower()}"
    
    with Image.open(source_filepath) as image_object:
        if target_format.upper() in ["JPG", "JPEG", "JFIF"] and image_object.mode in ("RGBA", "LA", "P"):
            image_object = image_object.convert("RGB")
        image_object.save(target_filepath, format=target_format.upper())

root_window = tkinter.Tk()
root_window.title("Image Converter")
root_window.geometry("400x180")

file_extension = file_path.split(".")[-1]
available_formats = get_available_target_formats(file_extension)

path_label = tkinter.Label(root_window, text=f"File: {file_path}", wraplength=380, anchor="w", justify="left")
path_label.pack(padx=10, pady=10, fill="x")

selected_format_variable = tkinter.StringVar(root_window)
if available_formats:
    selected_format_variable.set(available_formats[0])

format_dropdown = ttk.Combobox(root_window, textvariable=selected_format_variable, values=available_formats, state="readonly")
format_dropdown.pack(padx=10, pady=10, fill="x")

def handle_conversion_action():
    target_format = selected_format_variable.get()
    convert(file_path, target_format)
    root_window.destroy()

convert_button = tkinter.Button(root_window, text="Convert", command=handle_conversion_action)
convert_button.pack(padx=10, pady=15)

root_window.mainloop()