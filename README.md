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
>>> from sh import tree
>>> tree('test.zr3')
test.zr3
└── zarr.json
0 directories, 1 file

```
