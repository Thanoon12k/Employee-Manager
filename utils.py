import os

def get_folder_tree(start_folder, exclude_folders=None):
    if exclude_folders is None:
        exclude_folders = []

    tree = []

    for root, dirs, files in os.walk(start_folder):
        path = root.split(os.sep)
        subtree = tree

        # Check if any folder in the path should be excluded
        if any(folder in path for folder in exclude_folders):
            continue

        level = len(path) - len(start_folder.split(os.sep))
        indent = '│   ' * (level - 1) + '│── ' if level > 0 else ''
        subtree.append(f"{indent}{os.path.basename(root)}/")

        # Modify dirs in-place to exclude specified folders
        dirs[:] = [d for d in dirs if d not in exclude_folders]

        for file in files:
            subtree.append(f"{'│   ' * level}│── {file}")

    return '\n'.join(tree)

if __name__ == "__main__":
    start_folder = os.path.dirname(os.path.abspath(__file__))
    exclude = ['folder_to_exclude1', 'folder_to_exclude2']
    tree = get_folder_tree(start_folder, exclude)
    with open('parent_name.txt', 'w', encoding='utf-8') as f:
        f.write(tree)