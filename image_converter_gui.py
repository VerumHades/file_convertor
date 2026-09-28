import os
import sys
import tkinter
from tkinter import messagebox
from tkinter import ttk
from PIL import Image

SUPPORTED_FORMATS = {"png", "jpg", "jpeg", "jfif", "webp"}

def filter_and_validate_input_files(raw_file_paths):
    """Filter raw input file paths and return only those with supported extensions."""
    valid_file_paths = []
    invalid_file_count = 0

    for file_path in raw_file_paths:
        file_extension = file_path.split(".")[-1].lower()
        if file_extension in SUPPORTED_FORMATS:
            valid_file_paths.append(file_path)
        else:
            invalid_file_count += 1

    return valid_file_paths, invalid_file_count


def get_available_target_formats():
    """Return the list of all supported target image formats."""
    return ["PNG", "JPG", "JPEG", "JFIF", "WEBP"]


def convert_single_image(source_filepath, target_format):
    """Convert a single image file to the specified target format."""
    base_path, _ = source_filepath.rsplit(".", 1)
    target_filepath = f"{base_path}.{target_format.lower()}"
    
    with Image.open(source_filepath) as image_object:
        if target_format.upper() in ["JPG", "JPEG", "JFIF"] and image_object.mode in ("RGBA", "LA", "P"):
            image_object = image_object.convert("RGB")
        image_object.save(target_filepath, format=target_format.upper())


raw_arguments = sys.argv[1:]
valid_files, invalid_count = filter_and_validate_input_files(raw_arguments)

root_window = tkinter.Tk()
root_window.title("Batch Image Converter")
root_window.geometry("450x350")

if invalid_count > 0:
    messagebox.showwarning(
        "Invalid Files Discarded",
        f"{invalid_count} file(s) with unsupported formats were automatically discarded."
    )

if not valid_files:
    messagebox.showerror("Error", "No valid image files provided for conversion.")
    sys.exit(1)

instruction_label = tkinter.Label(root_window, text="Files scheduled for conversion:", anchor="w", justify="left")
instruction_label.pack(padx=10, pady=(10, 0), fill="x")

file_listbox_frame = tkinter.Frame(root_window)
file_listbox_frame.pack(padx=10, pady=5, fill="both", expand=True)

file_scrollbar = tkinter.Scrollbar(file_listbox_frame, orient="vertical")
file_scrollbar.pack(side="right", fill="y")

file_listbox = tkinter.Listbox(file_listbox_frame, yscrollcommand=file_scrollbar.set, selectmode="extended")
for valid_file in valid_files:
    file_listbox.insert("end", valid_file)
file_listbox.pack(side="left", fill="both", expand=True)

file_scrollbar.config(command=file_listbox.yview)

format_selection_frame = tkinter.Frame(root_window)
format_selection_frame.pack(padx=10, pady=10, fill="x")

format_label = tkinter.Label(format_selection_frame, text="Target Format:")
format_label.pack(side="left", padx=(0, 10))

available_formats = get_available_target_formats()
selected_format_variable = tkinter.StringVar(root_window)
selected_format_variable.set(available_formats[0])

format_dropdown = ttk.Combobox(format_selection_frame, textvariable=selected_format_variable, values=available_formats, state="readonly")
format_dropdown.pack(side="left", fill="x", expand=True)

progress_label = tkinter.Label(root_window, text="", fg="blue")
progress_label.pack(padx=10, pady=5)


def handle_batch_conversion_action():
    """Execute batch conversion for all listed files with collision handling."""
    target_format = selected_format_variable.get()
    total_files = len(valid_files)
    global_collision_action = None

    for index, source_filepath in enumerate(valid_files, start=1):
        progress_label.config(text=f"Converting ({index}/{total_files}): {os.path.basename(source_filepath)}")
        root_window.update_idletasks()

        base_path, _ = source_filepath.rsplit(".", 1)
        target_filepath = f"{base_path}.{target_format.lower()}"

        if os.path.exists(target_filepath):
            if global_collision_action == "Replace all":
                pass
            elif global_collision_action == "Ignore all":
                continue
            else:
                collision_dialog = tkinter.Toplevel(root_window)
                collision_dialog.title("File Collision")
                collision_dialog.geometry("350x150")
                collision_dialog.grab_set()

                collision_message = tkinter.Label(
                    collision_dialog,
                    text=f"File already exists:\n{os.path.basename(target_filepath)}\nChoose an action:",
                    justify="center"
                )
                collision_message.pack(padx=10, pady=10)

                user_choice = tkinter.StringVar(value="")

                def set_choice(choice):
                    user_choice.set(choice)
                    collision_dialog.destroy()

                button_frame = tkinter.Frame(collision_dialog)
                button_frame.pack(padx=10, pady=10)

                tkinter.Button(button_frame, text="Replace", command=lambda: set_choice("Replace")).grid(row=0, column=0, padx=2, pady=2)
                tkinter.Button(button_frame, text="Ignore", command=lambda: set_choice("Ignore")).grid(row=0, column=1, padx=2, pady=2)
                tkinter.Button(button_frame, text="Replace All", command=lambda: set_choice("Replace all")).grid(row=1, column=0, padx=2, pady=2)
                tkinter.Button(button_frame, text="Ignore All", command=lambda: set_choice("Ignore all")).grid(row=1, column=1, padx=2, pady=2)

                root_window.wait_window(collision_dialog)
                
                chosen_action = user_choice.get()
                if chosen_action in ("Replace all", "Ignore all"):
                    global_collision_action = chosen_action

                if chosen_action in ("Ignore", "Ignore all"):
                    continue

        convert_single_image(source_filepath, target_format)

    progress_label.config(text="Conversion complete!")
    root_window.update_idletasks()
    root_window.after(1000, root_window.destroy)


convert_button = tkinter.Button(root_window, text="Convert All", command=handle_batch_conversion_action)
convert_button.pack(padx=10, pady=10)

root_window.mainloop()