from filefunctions import copy_static_to_public
from functions import generate_pages_recursively


def main():
    copy_static_to_public()
    generate_pages_recursively("content", "template.html", "public")


main()
