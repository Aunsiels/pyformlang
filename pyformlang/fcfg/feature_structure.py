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
            if path:
                feature = self.get_feature_by_path(path)
                value = feature.value
                if value is None:
                    value = id(feature)
                res.append(".".join(path) + "=" + str(value))
        return " | ".join(res)

    @classmethod
    def from_text(cls, text, structure_variables=None):
        if structure_variables is None:
            structure_variables = dict()
        preprocessed_conditions = preprocess_conditions(text)
        return create_feature_structure(preprocessed_conditions, structure_variables)


def find_closing_bracket(condition, start):
    counter = 0
    pos = start
    for x in condition[start:]:
        if x == "[":
            counter += 1
        elif x == "]":
            counter -= 1
        if counter == 0:
            return pos
        pos += 1
    return -1


def preprocess_conditions(conditions, start=0, end=-1):
    conditions = conditions.strip()
    res = []
    reading_feature = True
    current_feature = ""
    current_value = ""
    pos = start
    end = len(conditions) if end == -1 else end
    while pos < end:
        current = conditions[pos]
        if current == "=":
            reading_feature = False
            pos += 1
        elif reading_feature:
            current_feature += current
            pos += 1
        elif current == "[":
            end = find_closing_bracket(conditions, pos)
            if end == -1:
                raise Exception()
            current_value = preprocess_conditions(conditions, pos + 1, end)
            pos = end + 1
        elif current == ",":
            reading_feature = True
            if type(current_value) == str:
                current_value = current_value.strip()
            res.append((current_feature.strip(), current_value))
            current_feature = ""
            current_value = ""
            pos += 1
        else:
            current_value += current
            pos += 1
    if current_feature.strip():
        if type(current_value) == str:
            current_value = current_value.strip()
        res.append((current_feature.strip(), current_value))
    return res


def create_feature_structure(conditions, structure_variables):
    fs = FeatureStructure()
    for feature, value in conditions:
        if type(value) == str:
            if value[0] != "?":
                fs.add_content(feature, FeatureStructure(value))
            elif value[1:] in structure_variables:
                fs.add_content(feature, structure_variables[value[1:]])
            else:
                new_fs = FeatureStructure()
                fs.add_content(feature, new_fs)
                structure_variables[value[1:]] = new_fs
        else:
            fs.add_content(feature, create_feature_structure(value, structure_variables))
    return fs
