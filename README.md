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

## Installation
```python
    $  pip3 install semvermanager
```
   
## Docs

Full class docs are on readthedocs.io.

## Source code

Can be found on [github.com](https://github.com/jdrumgoole/semvermanager)

**Author**: *jdrumgoole* on [GitHub](https://github.com/jdrumgoole)
