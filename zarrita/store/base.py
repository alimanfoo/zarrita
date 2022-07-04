from abc import ABC, ABCMeta, abstractmethod
from typing import NamedTuple, Optional, Union, Literal
import logging

Key = str
Range = tuple[int, int]
Value = bytes

logger = logging.getLogger(__name__)


class Store(ABC):
    """Do not subclass this directly.

    Instead, subclass ReadableStore, ListableStore and WriteableStore.
    """

    is_readable = False
    is_writeable = False
    is_listable = False


class ZarrKeyError(KeyError):
    pass


class ReadableStore(Store, metaclass=ABCMeta):
    is_readable = True

    @abstractmethod
    def _get(self, key: Key) -> Value:
        """Raises ZarrKeyError if key does not exist"""
        pass

    def get(self, key: Key, default: Optional[Value] = None) -> Value:
        try:
            val = self._get(key)
        except ZarrKeyError:
            if default is None:
                raise
            val = default
        return val

    def get_partial_values(
        self, key_ranges: list[tuple[Key, Range]]
    ) -> list[Optional[Value]]:
        out: list[Optional[Value]] = []
        for k, r in key_ranges:
            try:
                v = self.get(k)
            except KeyError:
                out.append(None)
                continue
            out.append(v[r[0] : r[1]])
        return out


class ListDirResult(NamedTuple):
    keys: set[Key]
    prefixes: set[Key]


class ListableStore(Store, metaclass=ABCMeta):
    is_listable = True

    @abstractmethod
    def list(self) -> set[Key]:
        pass

    def list_prefix(self, prefix: Key) -> set[Key]:
        if not prefix.endswith("/"):
            logger.warning(
                "Behavior of list_prefix is undefined "
                "if the key does not end in '/': %s",
                prefix,
            )

        out = set()
        for key in self.list():
            if key.startswith(prefix):
                out.add(key)
        return out

    def list_dir(self, prefix: Key) -> ListDirResult:
        pref_len = len(prefix)
        out = ListDirResult(set(), set())
        for key in self.list_prefix(prefix):
            tail = key[pref_len:]
            split = tail.split("/")
            to_add = prefix + split[0]
            if len(split) > 1:
                out.prefixes.add(to_add)
            else:
                out.keys.add(to_add)
        return out


class WriteableStore(Store, metaclass=ABCMeta):
    is_writeable = True

    @abstractmethod
    def set(self, key: Key, value: Value) -> None:
        pass

    def set_partial_values(
        self, key_start_values: list[tuple[Key, int, Value]]
    ) -> None:
        if not isinstance(self, ReadableStore):
            raise NotImplementedError(
                "Default implementation for WriteableStore.set_partial_values "
                "is only available for ReadableStores"
            )

        for key, start, value in key_start_values:
            orig = self.get(key)
            new = orig[:start] + value + orig[start + len(value) :]
            self.set(key, new)

    @abstractmethod
    def erase(self, key: Key) -> None:
        pass

    def erase_values(self, keys: set[Key]) -> None:
        for key in keys:
            self.erase(key)

    def erase_prefix(self, prefix: Key) -> None:
        if not isinstance(self, ListableStore):
            raise NotImplementedError(
                "Default implementation for WriteableStore.erase_prefix "
                " is only available for ListableStores"
            )

        keys = self.list_prefix(prefix)
        self.erase_values(keys)
