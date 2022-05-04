# Copied from https://realpython.com/directory-tree-generator-python/

import os
import pathlib

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "  "


class _TreeGenerator:
    def __init__(self, root_dir):

        self._root_dir = pathlib.Path(root_dir)

        self._tree = []

    def _tree_body(self, directory, prefix=""):

        entries = directory.iterdir()

        entries = sorted(entries, key=lambda entry: entry.is_file())

        entries_count = len(entries)

        for index, entry in enumerate(entries):

            connector = ELBOW if index == entries_count - 1 else TEE

            if entry.is_dir():

                self._add_directory(entry, index, entries_count, prefix, connector)

            else:

                self._add_file(entry, prefix, connector)

    def _add_directory(self, directory, index, entries_count, prefix, connector):

        self._tree.append(f"{prefix}{connector} {directory.name}{os.sep}")

        prefix += PIPE_PREFIX if index != entries_count - 1 else SPACE_PREFIX
        self._tree_body(
            directory=directory,
            prefix=prefix,
        )

        self._tree.append(prefix.rstrip())

    def _add_file(self, file, prefix, connector):

        self._tree.append(f"{prefix}{connector} {file.name}")

    def build_tree(self):

        self._tree_head()

        self._tree_body(self._root_dir)

        return self._tree

    def _tree_head(self):

        self._tree.append(f"{self._root_dir}{os.sep}")

        self._tree.append(PIPE)


class DirectoryTree:
    def __init__(self, root_dir):
        self._generator = _TreeGenerator(root_dir)

    def generate(self):
        tree = self._generator.build_tree()
        ents = [f"{i}\n" for i in tree]
        return "".join(ents)


def gentree(root_dir):
    tree = DirectoryTree(root_dir)
    return tree.generate()
