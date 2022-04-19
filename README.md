# monotable

ASCII table with per column format specs, multi-line content,
formatting directives, column width control.

### default branch status

[![](https://img.shields.io/pypi/l/monotable.svg)](http://www.apache.org/licenses/LICENSE-2.0)
[![](https://img.shields.io/pypi/v/monotable.svg)](https://pypi.python.org/pypi/monotable)
[![](https://img.shields.io/pypi/pyversions/monotable.svg)](https://pypi.python.org/pypi/monotable)

[![CI Test](https://github.com/tmarktaylor/monotable/actions/workflows/ci.yml/badge.svg)](https://github.com/tmarktaylor/monotable/actions/workflows/ci.yml)
[![readthedocs](https://readthedocs.org/projects/monotable/badge/?version=latest)](https://monotable.readthedocs.io/en/latest/?badge=latest)


[Docs](https://monotable.readthedocs.io/en/latest/) |
[Repos](https://github.com/tmarktaylor/monotable) |
[Codecov](https://codecov.io/gh/tmarktaylor/monotable?branch=master) |
[License](https://github.com/tmarktaylor/monotable/blob/master/LICENSE)

### Sample usage
```python
from monotable import mono

headings = ["purchased\nparrot\nheart rate", "life\nstate"]

# > is needed to right align None cell since it auto-aligns to left.
# monotable uses empty string to format the second column.
formats = [">(none=rest).0f"]
cells = [
    [0, "demised"],
    [0.0, "passed on"],
    [None, "is no more"],
    [-1],
    [0, "ceased to be"],
]

print(
    mono(
        headings,
        formats,
        cells,
        title="Complaint\n(registered)",
        # top guideline is equals, heading is period, bottom is omitted.
        guideline_chars="=. ",
    )
)
```

sample output:
```
       Complaint
      (registered)
========================
 purchased
    parrot  life
heart rate  state
........................
         0  demised
         0  passed on
      rest  is no more
        -1
         0  ceased to be
```
