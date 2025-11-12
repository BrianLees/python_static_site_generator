import os
from pathlib import Path
import shutil


def delete_public_dir():
    if os.path.exists("public"):
        print("Removing 'public/' directory.")
        shutil.rmtree("public", ignore_errors=True)


def copy_file_to_public(source, destination):
    print(f"Scanning '{source}'...")
    contents = os.listdir(source)
    if not os.path.exists(destination):
        print(f"Creating '{destination}' directory.")
        os.mkdir(destination)
    for item in contents:
        item_path = f"{source}/{item}"
        print(f"Processing '{item_path}'...")
        if os.path.isdir(item_path):
            new_source = item_path
            new_destination = f"{destination}/{item}"
            copy_file_to_public(new_source, new_destination)
        elif os.path.isfile(item_path):
            print(f"Copying '{item_path}' to '{destination}/{item}'")
            shutil.copy(item_path, f"{destination}/{item}")
        else:
            print(f"{item_path}: Showing as neither a file or a directory")


def copy_static_to_public():
    delete_public_dir()
    os.mkdir("public")
    copy_file_to_public("static", "public")


if __name__ == "__main__":
    # Example usage for your case:
    copy_static_to_public()
