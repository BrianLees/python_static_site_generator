from __future__ import annotations
import logging
import os
from pathlib import Path
import shutil

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(message)s"
)


def delete_dir_contents(path):
    """Delete all files/subdirectories inside public"""
    if not path.exists():
        return
    for child in path.iterdir():
        if child.is_dir():
            shutil.rmtree(child)   # removes dir tree
        else:
            child.unlink()         # removes file


def copy_tree(src, dst):
    """
    Recursively copy the contents of `src` into `dst`, creating directories as needed.
    Logs each file copied.
    """
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            copy_tree(item, target)  # recurse
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)  # preserves mtime/metadata
            logging.info("Copied: %s -> %s", item, target)


def copy_static_to_public(src_dir="static", dst_dir="public"):
    """
    Deletes all contents of `dst_dir`, then copies everything from `src_dir` into it.
    Example: copy_static_to_public('static', 'public')
    """
    src = Path(src_dir).resolve()
    dst = Path(dst_dir).resolve()

    if not src.exists() or not src.is_dir():
        raise ValueError(
            f"Source directory does not exist or is not a directory: {src}")

    # Guard: never let src and dst be the same directory
    if src == dst:
        raise ValueError(
            "Source and destination directories must be different.")

    # Ensure destination exists, then clear its contents
    dst.mkdir(parents=True, exist_ok=True)
    logging.info("Cleaning destination: %s", dst)
    delete_dir_contents(dst)

    # Copy recursively
    logging.info("Copying from %s to %s", src, dst)
    copy_tree(src, dst)
    logging.info("Done.")


if __name__ == "__main__":
    # Example usage for your case:
    copy_static_to_public()
