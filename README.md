*qbuild-jupyter* is a convert system for our jupyter challenges.

# Installation

For installing or updating qbuild, run the following commands:

```bash
$ git clone this repository
$ cd qbuild-jupyter
$ sudo pip3 install . 
```

---

# [Examples]('example.py'):

### Convert initial directory in path:

```python
from qbuild_jupyter import converter

nonquera_extract_dir_path, nonquera_extract_zip_path = converter.convert_initial_to_nonquera_in_path(
    path='/path/to/initial/dir',
    mode='dir',
    nonquera_dir='/path/to/where/you/want/dir'
)

```

### Convert initial zip in path:

```python
from qbuild_jupyter import converter

nonquera_extract_dir_path, nonquera_extract_zip_path = converter.convert_initial_to_nonquera_in_path(
    path='/path/to/initial.zip',
    mode='zip',
    nonquera_dir='/path/to/where/you/want/dir'
)

```


### Convert in temporary file:
```python

from qbuild_jupyter import converter

# convert initial directory in temporary file
temp_file = converter.convert_initial_to_nonquera_in_temp_file(
    path='/path/to/initial/dir',
    mode='dir',
)


# convert initial zip in temporary file
temp_file = converter.convert_initial_to_nonquera_in_temp_file(
    path='/path/to/initial.zip',
    mode='zip',
)

```


