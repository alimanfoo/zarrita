import fsspec
from .base import (
    ReadableStore,
    ListableStore,
    WriteableStore,
    Key,
    Value,
    ZarrKeyError,
    ListDirResult,
)


class FileSystemStore(ReadableStore, ListableStore, WriteableStore):

    # TODO ultimately replace this with the fsspec FSMap class, but for now roll
    # our own implementation in order to be able to add some extra methods for
    # listing keys.

    def __init__(self, url: str, **storage_options):
        assert isinstance(url, str)

        # instantiate file system
        fs, root = fsspec.core.url_to_fs(url, **storage_options)
        self.fs = fs
        self.root = root.rstrip("/")

    def _get(self, key: Key) -> Value:
        path = f"{self.root}/{key}"
        try:
            value = self.fs.cat(path)
        except (FileNotFoundError, IsADirectoryError, NotADirectoryError) as e:
            raise ZarrKeyError(str(e))

        return value

    def set(self, key: str, value: bytes) -> None:
        assert isinstance(key, str)
        path = f"{self.root}/{key}"

        # ensure parent folder exists
        # noinspection PyProtectedMember
        self.fs.mkdirs(self.fs._parent(path), exist_ok=True)

        # write data
        with self.fs.open(path, "wb") as f:
            f.write(value)

    def erase(self, key: str) -> None:
        assert isinstance(key, str)
        path = f"{self.root}/{key}"
        self.fs.rm(path)

    def list(self):
        out = set()
        for item in self.fs.find(self.root, withdirs=False, detail=False):
            out.add(item.split(self.root + "/")[1])
        return out

    def list_prefix(self, prefix: str) -> set[str]:
        assert isinstance(prefix, str)
        assert prefix[-1] == "/"
        path = f"{self.root}/{prefix}"
        try:
            items = self.fs.find(path, withdirs=False, detail=False)
        except FileNotFoundError:
            return []
        return {item.split(path)[1] for item in items}

    def list_dir(self, prefix: str = ""):
        assert isinstance(prefix, str)
        if prefix:
            assert prefix[-1] == "/"

        # setup result
        keys: set[str] = set()
        prefixes: set[str] = set()

        # attempt to list directory
        path = f"{self.root}/{prefix}"
        try:
            ls = self.fs.ls(path, detail=True)
        except FileNotFoundError:
            return ListDirResult(keys=keys, prefixes=prefixes)

        # build result
        for item in ls:
            name = item["name"].split(path)[1]
            if item["type"] == "file":
                keys.add(name)
            elif item["type"] == "directory":
                prefixes.add(name)

        return ListDirResult(keys=keys, prefixes=prefixes)

    def __repr__(self) -> str:
        protocol = self.fs.protocol
        if isinstance(protocol, tuple):
            protocol = protocol[-1]
        return f"{protocol}://{self.root}"
