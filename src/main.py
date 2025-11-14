import sys
from filefunctions import copy_static_to_public
from functions import generate_pages_recursively


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_static_to_public()
    generate_pages_recursively("content", "template.html", "docs", basepath)


main()
