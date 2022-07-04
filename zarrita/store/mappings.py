from collections.abc import MutableMapping, Mapping

from .base import ReadableStore, ListableStore, WriteableStore, Key, Value, ZarrKeyError


class MappingStore(ReadableStore, ListableStore):
    mapping: Mapping[Key, Value]

    def __init__(self, mapping: Mapping) -> None:
        self.mapping = mapping

    def _get(self, key: Key) -> Value:
        try:
            return self.mapping[key]
        except KeyError as e:
            raise ZarrKeyError(str(e))

    def list(self) -> set[Key]:
        return set(self.mapping)


class MutableMappingStore(MappingStore, WriteableStore):
    mapping: MutableMapping[Key, Value]

    def __init__(self, mapping: MutableMapping) -> None:
        super().__init__(mapping)

    def set(self, key: Key, value: Value) -> None:
        self.mapping[key] = value

    def erase(self, key: Key) -> None:
        del self.mapping[key]
