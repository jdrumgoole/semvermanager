semvermmanager
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
    str TAG    # one of "alpha", "beta", "prod". 
```

Versions may be bumped by a single increment using any of the 
`bump` functions. Bumping a PATCH value simply increments it.
Bumping a MINOR value zeros the PATCH value and bumping a MAJOR
zeros the MINOR and the PATCH value.

`semvermanager` only supports Python 3.6 and greater.

## semvergen script
The package includes a command line script for generating versions.

```bash
$ ./semvergen -h
usage: semvergen [-h] [--filename FILENAME] [--version VERSION] [--make]
                 [--bump {major,minor,patch,tag}] [--getversion] [--overwrite]
                 [--update]

optional arguments:
  -h, --help            show this help message and exit
  --filename FILENAME   File to use as version file [default: VERSION]
  --version VERSION     Specify a version in the form major.minor.patch-tag
  --make                Make a new version file
  --bump {major,minor,patch,tag}
                        Bump a version field
  --getversion          Report the current version in the specified file
  --overwrite           overwrite files without checking
  --update              Update multiple version strings in file

```
## Installation
```python
    $  pip3 install semvermanager
```
   
## Docs

Full class docs are on readthedocs.io.

## Source code

Can be found on [github.com](https://github.com/jdrumgoole/semvermanager)

**Author**: *jdrumgoole* on [GitHub](https://github.com/jdrumgoole)
