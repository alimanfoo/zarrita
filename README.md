**Here be dragons.**

Ensure blank slate:

```
>>> import shutil
>>> shutil.rmtree('test.zr3')
 
```

Create a new hierarchy stored on the local file system:

```
>>> import zarr_v3
>>> h = zarr_v3.create_hierarchy('test.zr3')
>>> h
<zarr_v3 Hierarchy>
>>> from sh import tree, cat
>>> tree('test.zr3', '-n')
test.zr3
└── zarr.json
<BLANKLINE>
0 directories, 1 file
<BLANKLINE>

>>> cat('test.zr3/zarr.json')
{
    "zarr_format": "https://purl.org/zarr/spec/protocol/core/3.0",
    "metadata_encoding": "application/json",
    "extensions": []
}

```

Create an array:

```
>>> a1 = h.create_array('/foo/bar', shape=(100, 10), dtype='i4', chunks=(20, 5), compressor=None)
>>> a1
<zarr_v3 Array /foo/bar>
>>> tree('test.zr3', '-n')
test.zr3
├── meta
│   └── root
│       └── foo
│           └── bar.array
└── zarr.json
<BLANKLINE>
3 directories, 2 files
<BLANKLINE>

>>> cat('test.zr3/meta/root/foo/bar.array')
{
    "shape": [
        100,
        10
    ],
    "data_type": "<i4",
    "chunk_grid": {
        "type": "regular",
        "chunk_shape": [
            20,
            5
        ]
    },
    "chunk_memory_layout": "C",
    "compressor": null,
    "fill_value": null,
    "extensions": [],
    "attributes": null
}

```