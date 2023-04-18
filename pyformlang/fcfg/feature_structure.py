from typing import Any, List


class ContentAlreadyExistsException(Exception):
    """Exception raised when we want to add a content that already exists"""


class PathDoesNotExistsException(Exception):
    """Raised when looking for a path that does not exist"""


class FeatureStructuresNotCompatibleException(Exception):
    """Raised when trying to unify uncompatible structures"""


class FeatureStructure:

    def __init__(self, value=None):
        self._content = dict()
        self._value = value
        self._pointer = None

    def copy(self, already_copied=None):
        if already_copied is None:
            already_copied = dict()
        if self in already_copied:
            return already_copied[self]
        new_fs = FeatureStructure(self.value)
        if self._pointer is not None:
            pointer_copy = self._pointer.copy(already_copied)
            new_fs.pointer = pointer_copy
        for feature in self._content:
            new_fs.content[feature] = self._content[feature].copy(already_copied)
        already_copied[self] = new_fs
        return new_fs

    @property
    def content(self) -> Any:
        """Gets the content of the current node"""
        return self._content

    @property
    def pointer(self) -> Any:
        """Gets the pointer of the current node"""
        return self._pointer

    @pointer.setter
    def pointer(self, new_pointer):
        self._pointer = new_pointer


    @property
    def value(self) -> Any:
        """Gets the value associated to the current node"""
        return self._value if self.pointer is None else self.pointer.value

    def add_content(self, content_name: str, feature_structure: "FeatureStructure"):
        if content_name in self._content:
            raise ContentAlreadyExistsException()
        self._content[content_name] = feature_structure

    def add_content_path(self, content_name: str, feature_structure: "FeatureStructure", path: List[str]):
        to_modify = self.get_feature_by_path(path)
        to_modify.add_content(content_name, feature_structure)

    def get_dereferenced(self):
        return self._pointer.get_dereferenced() if self._pointer is not None else self

    def get_feature_by_path(self, path: List[str] = None):
        if not path or path is None:
            return self
        current = self.get_dereferenced()
        if path[0] not in current.content:
            raise PathDoesNotExistsException()
        return current._content[path[0]].get_feature_by_path(path[1:])

    def unify(self, other: "FeatureStructure"):
        current_dereferenced = self.get_dereferenced()
        other_dereferenced = other.get_dereferenced()
        if current_dereferenced == other_dereferenced:
            return
        if len(current_dereferenced.content) == 0 and len(other_dereferenced.content) == 0:
            # We have a simple feature
            if current_dereferenced.value == other_dereferenced.value:
                current_dereferenced.pointer = other_dereferenced
            elif current_dereferenced.value is None:
                current_dereferenced.pointer = other_dereferenced
            elif other_dereferenced.value is None:
                other_dereferenced.pointer = current_dereferenced
            else:
                raise FeatureStructuresNotCompatibleException()
        else:
            other_dereferenced.pointer = current_dereferenced
            for feature in other_dereferenced.content:
                if feature not in current_dereferenced.content:
                    current_dereferenced.content[feature] = FeatureStructure()
                current_dereferenced.content[feature].unify(other_dereferenced.content[feature])

    def subsumes(self, other: "FeatureStructure"):
        current_dereferenced = self.get_dereferenced()
        other_dereferenced = other.get_dereferenced()
        if current_dereferenced.value != other_dereferenced.value:
            return False
        for feature in current_dereferenced.content:
            if feature not in other_dereferenced.content:
                return False
            if not current_dereferenced.content[feature].subsumes(other_dereferenced.content[feature]):
                return False
        return True

    def get_all_paths(self):
        res = []
        for feature in self._content:
            paths = self._content[feature].get_all_paths()
            for path in paths:
                res.append([feature] + path)
        if not res:
            res.append([])
        return res

    def __repr__(self):
        res = []
        for path in self.get_all_paths():
            res.append(".".join(path) + "=" + str(self.get_feature_by_path(path).value))
        return " | ".join(res)
