import os


def create_file(
    module_path: str = None,
    content: str = None,
    file_extension: str = "md",
):
    """
    Creates a documentation file for the given item.

    Args:
        item: The item to create the documentation file for.
        content (str, optional): The content to be written in the file. Defaults to None.

    Returns:
        str: The file path of the created documentation file.

    """
    os.makedirs(module_path, exist_ok=True)
    file_path = os.path.join(module_path, file_extension)
    with open(file_path, "w") as file:
        file.write(content)
    return file_path
