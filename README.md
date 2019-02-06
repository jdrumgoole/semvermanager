semvermanager
============================================================
`semvermamager` exports a single class `Version` which implements
a restricted subset of the [SEMVER](http://semver.org) standard.

`Version` defines a Semantic version using the following field
structure:

```python
    # MAJOR.MINOR.PATCH-TAG
    
    int MAJOR  # 0->N
    int MINOR  # 0->N
    int PATCH  # 0-N
    str TAG    # one of "alpha", "beta". 
    int TAG_VERSION # a version number appended to alpha or beta. 
```

Versions may be bumped by a single increment using any of the 
`bump` functions. Bumping a PATCH value simply increments it.
Bumping a MINOR value zeros the PATCH value and bumping a MAJOR
zeros the MINOR and the PATCH value.

`semvermanager` only supports Python 3.6 and greater.

## semvermgr script
The package includes a command line script for generating versions.

```bash
$ semvermgr -h
usage: semvermgr.py [-h] [--version VERSION] [--make]
                    [--bump {major,minor,patch,tag,tag_version}]
                    [--getversion] [--bareversion] [--overwrite] [--update]
                    [--label LABEL] [--separator SEPARATOR]
                    [filenames [filenames ...]]

positional arguments:
  filenames             Files to use as version file

optional arguments:
  -h, --help            show this help message and exit
  --version VERSION     Specify a version in the form major.minor.patch-tag
  --make                Make a new version file
  --bump {major,minor,patch,tag,tag_version}
                        Bump a version field
  --getversion          Report the current version in the specified file
  --bareversion         Return the unquoted version strin with VERSION=
  --overwrite           overwrite files without checking [default: False]
  --update              Update multiple version strings in file
  --label LABEL         field used to determine which line is the version line
                        [default: VERSION]
  --separator SEPARATOR
                        Character used to separate the version label from the
                        version [default: =]
```
## Installation
```python
    $  pip3 install semvermanager
```
   
## Docs

Full docs are on [readthedocs.io](https://semvermanager.readthedocs.io/en/latest/).

## Source code

Can be found on [github.com](https://github.com/jdrumgoole/semvermanager)

**Author**: *jdrumgoole* on [GitHub](https://github.com/jdrumgoole)
