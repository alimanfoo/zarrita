**Here be dragons.** Minimal exploratory implementation of the Zarr version 3.0 core protocol. 
This is a technical spike, not for production use.

Ensure blank slate:

```
>>> import shutil
>>> shutil.rmtree('test.zr3', ignore_errors=True)
 
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

Access a previously created hierarchy:

```
>>> h = zarr_v3.get_hierarchy('test.zr3')
>>> h
<zarr_v3 Hierarchy>

```

Create an array:

```
>>> a = h.create_array('/arthur/dent', shape=(5, 10), dtype='i4', chunk_shape=(2, 5), compressor=None, attrs={'question': 'life', 'answer': 42})
>>> a
<zarr_v3 Array /arthur/dent>
>>> a.path
'/arthur/dent'
>>> a.name
'dent'
>>> a.ndim
2
>>> a.shape
(5, 10)
>>> a.dtype
dtype('int32')
>>> a.chunk_shape
(2, 5)
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
        5,
        10
    ],
    "data_type": "<i4",
    "chunk_grid": {
        "type": "regular",
        "chunk_shape": [
            2,
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
>>> g.path
'/tricia/mcmillan'
>>> g.name
'mcmillan'
>>> g.attrs
{'heart': 'gold', 'improbability': 'infinite'}
>>> tree('test.zr3', '-n')
test.zr3
├── meta
│   └── root
│       ├── arthur
│       │   └── dent.array
│       └── tricia
│           └── mcmillan.group
└── zarr.json
<BLANKLINE>
4 directories, 3 files
<BLANKLINE>

>>> cat('test.zr3/meta/root/tricia/mcmillan.group')
{
    "extensions": [],
    "attributes": {
        "heart": "gold",
        "improbability": "infinite"
    }
}

```

Access an array:

```
>>> a = h['/arthur/dent']
>>> a
<zarr_v3 Array /arthur/dent>
>>> a.shape
(5, 10)
>>> a.dtype
dtype('int32')
>>> a.chunk_shape
(2, 5)
>>> a.compressor is None
True
>>> a.attrs
{'question': 'life', 'answer': 42}

```

Access an explicit group:

```
>>> g = h['/tricia/mcmillan']
>>> g
<zarr_v3 Group /tricia/mcmillan>
>>> g.attrs
{'heart': 'gold', 'improbability': 'infinite'}

```

Access implicit groups:

```
>>> h['/']
<zarr_v3 Group / (implied)>
>>> h['/arthur']
<zarr_v3 Group /arthur (implied)>
>>> h['/tricia']
<zarr_v3 Group /tricia (implied)>

```

Access nodes via groups:

```
>>> root = h['/']
>>> root
<zarr_v3 Group / (implied)>
>>> arthur = root['arthur']
>>> arthur
<zarr_v3 Group /arthur (implied)>
>>> arthur['dent']
<zarr_v3 Array /arthur/dent>
>>> tricia = root['tricia']
>>> tricia
<zarr_v3 Group /tricia (implied)>
>>> tricia['mcmillan']
<zarr_v3 Group /tricia/mcmillan>

```

Explore the hierarchy:

```
>>> h.list_children('/')
[{'name': 'arthur', 'type': 'implicit_group'}, {'name': 'tricia', 'type': 'implicit_group'}]
>>> h.list_children('/tricia')
[{'name': 'mcmillan', 'type': 'explicit_group'}]
>>> h.list_children('/tricia/mcmillan')
[]
>>> h.list_children('/arthur')
[{'name': 'dent', 'type': 'array'}]

```

Alternative way to explore the hierarchy:

```
>>> root = h['/']
>>> root
<zarr_v3 Group / (implied)>
>>> root.list_children()
[{'name': 'arthur', 'type': 'implicit_group'}, {'name': 'tricia', 'type': 'implicit_group'}]
>>> root['tricia'].list_children()
[{'name': 'mcmillan', 'type': 'explicit_group'}]
>>> root['tricia']['mcmillan'].list_children()
[]
>>> root['arthur'].list_children()
[{'name': 'dent', 'type': 'array'}]

```

Read and write data into an array:

```
>>> import numpy as np
>>> a = h['/arthur/dent']
>>> a
<zarr_v3 Array /arthur/dent>
>>> tree('test.zr3', '-n')
test.zr3
├── meta
│   └── root
│       ├── arthur
│       │   └── dent.array
│       └── tricia
│           └── mcmillan.group
└── zarr.json
<BLANKLINE>
4 directories, 3 files
<BLANKLINE>
>>> a[:, :]
array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype=int32)
>>> a[...]
array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype=int32)
>>> a[:]
array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], dtype=int32)
>>> a[0, :] = 42
>>> a[:]
array([[42, 42, 42, 42, 42, 42, 42, 42, 42, 42],
       [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
       [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
       [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
       [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0]], dtype=int32)
>>> tree('test.zr3', '-n')
test.zr3
├── data
│   └── arthur
│       └── dent
│           ├── 0.0
│           └── 0.1
├── meta
│   └── root
│       ├── arthur
│       │   └── dent.array
│       └── tricia
│           └── mcmillan.group
└── zarr.json
<BLANKLINE>
7 directories, 5 files
<BLANKLINE>
>>> a[:, 0] = 42
>>> a[:]
array([[42, 42, 42, 42, 42, 42, 42, 42, 42, 42],
       [42,  0,  0,  0,  0,  0,  0,  0,  0,  0],
       [42,  0,  0,  0,  0,  0,  0,  0,  0,  0],
       [42,  0,  0,  0,  0,  0,  0,  0,  0,  0],
       [42,  0,  0,  0,  0,  0,  0,  0,  0,  0]], dtype=int32)
>>> tree('test.zr3', '-n')
test.zr3
├── data
│   └── arthur
│       └── dent
│           ├── 0.0
│           ├── 0.1
│           ├── 1.0
│           └── 2.0
├── meta
│   └── root
│       ├── arthur
│       │   └── dent.array
│       └── tricia
│           └── mcmillan.group
└── zarr.json
<BLANKLINE>
7 directories, 7 files
<BLANKLINE>

>>> a[:] = 42
>>> a[:]
array([[42, 42, 42, 42, 42, 42, 42, 42, 42, 42],
       [42, 42, 42, 42, 42, 42, 42, 42, 42, 42],
       [42, 42, 42, 42, 42, 42, 42, 42, 42, 42],
       [42, 42, 42, 42, 42, 42, 42, 42, 42, 42],
       [42, 42, 42, 42, 42, 42, 42, 42, 42, 42]], dtype=int32)
>>> tree('test.zr3', '-n')
test.zr3
├── data
│   └── arthur
│       └── dent
│           ├── 0.0
│           ├── 0.1
│           ├── 1.0
│           ├── 1.1
│           ├── 2.0
│           └── 2.1
├── meta
│   └── root
│       ├── arthur
│       │   └── dent.array
│       └── tricia
│           └── mcmillan.group
└── zarr.json
<BLANKLINE>
7 directories, 9 files
<BLANKLINE>
>>> a[0, :] = np.arange(10)
>>> a[:]
array([[ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9],
       [42, 42, 42, 42, 42, 42, 42, 42, 42, 42],
       [42, 42, 42, 42, 42, 42, 42, 42, 42, 42],
       [42, 42, 42, 42, 42, 42, 42, 42, 42, 42],
       [42, 42, 42, 42, 42, 42, 42, 42, 42, 42]], dtype=int32)
>>> a[:, 0] = np.arange(0, 50, 10)
>>> a[:]
array([[ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9],
       [10, 42, 42, 42, 42, 42, 42, 42, 42, 42],
       [20, 42, 42, 42, 42, 42, 42, 42, 42, 42],
       [30, 42, 42, 42, 42, 42, 42, 42, 42, 42],
       [40, 42, 42, 42, 42, 42, 42, 42, 42, 42]], dtype=int32)
>>> a[:] = np.arange(50).reshape(5, 10)
>>> a[:]
array([[ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9],
       [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
       [20, 21, 22, 23, 24, 25, 26, 27, 28, 29],
       [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
       [40, 41, 42, 43, 44, 45, 46, 47, 48, 49]], dtype=int32)
>>> a[:, 0]
array([ 0, 10, 20, 30, 40], dtype=int32)
>>> a[:, 1]
array([ 1, 11, 21, 31, 41], dtype=int32)
>>> a[0, :]
array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], dtype=int32)
>>> a[1, :]
array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19], dtype=int32)
>>> a[:, 0:7]
array([[ 0,  1,  2,  3,  4,  5,  6],
       [10, 11, 12, 13, 14, 15, 16],
       [20, 21, 22, 23, 24, 25, 26],
       [30, 31, 32, 33, 34, 35, 36],
       [40, 41, 42, 43, 44, 45, 46]], dtype=int32)
>>> a[0:3, :]
array([[ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9],
       [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
       [20, 21, 22, 23, 24, 25, 26, 27, 28, 29]], dtype=int32)
>>> a[0:3, 0:7]
array([[ 0,  1,  2,  3,  4,  5,  6],
       [10, 11, 12, 13, 14, 15, 16],
       [20, 21, 22, 23, 24, 25, 26]], dtype=int32)
>>> a[1:4, 2:7]
array([[12, 13, 14, 15, 16],
       [22, 23, 24, 25, 26],
       [32, 33, 34, 35, 36]], dtype=int32)

```
