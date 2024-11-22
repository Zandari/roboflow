from PySide6 import QtWidgets
from .app import Application
import sys
import os
import glob
import subprocess



def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Application()
    app.setStyle('Fusion')
    app.exec()


def _get_folder_path(paths: list[str]) -> str:
    """Checks possible paths from cwd standpoint"""

    cwd = os.getcwd()
    for path in paths:
        full_path = os.path.join(cwd, path)
        if os.path.isdir(full_path):
            return full_path
    
    raise FileNotFoundError("Unable to find folder")



def convert():
    RESOURCES_PACKAGE = [
        "resources",
        "editor/resources"
    ]
    VIEWS_PACKAGE = [
        "views/blueprints",
        "editor/views/blueprints"
    ]

    resources_folder = _get_folder_path(RESOURCES_PACKAGE)
    views_folder = _get_folder_path(VIEWS_PACKAGE)

    ui_files = glob.glob(f"{resources_folder}/*.ui")
    print(f"{len(ui_files)} files in total")

    for ui_file_path in ui_files:
        print('-', ui_file_path)
        out_file_name = os.path.basename(ui_file_path) \
                            .removesuffix(".ui") + ".py"
        out_file_path = os.path.join(views_folder, out_file_name)
        subprocess.run(
            ["poetry", "run", "pyside6-uic", ui_file_path, "-o", out_file_path]
        )

    print("Done")


if __name__ == '__main__':
    main()
