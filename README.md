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
>>> a = h.create_array('/arthur/dent', shape=(100, 10), dtype='i4', chunk_shape=(20, 5), compressor=None, attrs={'question': 'life', 'answer': 42})
>>> a
<zarr_v3 Array /arthur/dent>
>>> a.path
'/arthur/dent'
>>> a.ndim
2
>>> a.shape
(100, 10)
>>> a.dtype
dtype('int32')
>>> a.chunk_shape
(20, 5)
>>> a.compressor is None
True
>>> a.attrs
{'question': 'life', 'answer': 42}
>>> tree('test.zr3', '-n')
test.zr3
├── meta
│   └── root
│       └── arthur
│           └── dent.array
└── zarr.json
<BLANKLINE>
3 directories, 2 files
<BLANKLINE>

>>> cat('test.zr3/meta/root/arthur/dent.array')
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
    "attributes": {
        "question": "life",
        "answer": 42
    }
}

```

Create a group:

```
>>> g = h.create_group('/tricia/mcmillan', attrs={'heart': 'gold', 'improbability': 'infinite'})
>>> g
<zarr_v3 Group /tricia/mcmillan>
>>> g.attrs
{'heart': 'gold', 'improbability': 'infinite'}

```

Access nodes in the hierarchy:

```
>>> a = h['/arthur/dent']
>>> a
<zarr_v3 Array /arthur/dent>
>>> a.shape
(100, 10)
>>> a.dtype
dtype('int32')
>>> a.chunk_shape
(20, 5)
>>> a.compressor is None
True
>>> a.attrs
{'question': 'life', 'answer': 42}
>>> g = h['/tricia/mcmillan']
>>> g
<zarr_v3 Group /tricia/mcmillan>
>>> g.attrs
{'heart': 'gold', 'improbability': 'infinite'}

```