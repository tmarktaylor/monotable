# monotable

ASCII table with per column format specs, multi-line content,
formatting directives, column width control.

[![](https://img.shields.io/pypi/l/monotable.svg)](http://www.apache.org/licenses/LICENSE-2.0)
[![PyPI](https://img.shields.io/pypi/v/monotable.svg)](https://pypi.python.org/pypi/monotable)
[![PyPI Python Versions](https://img.shields.io/pypi/pyversions/monotable.svg)](https://pypi.python.org/pypi/monotable)

### master branch status

[![Documentation Status](https://readthedocs.org/projects/monotable/badge/?version=latest)](https://monotable.readthedocs.io/en/latest/?badge=latest) on [Read the Docs](https://readthedocs.org)

[![Build Status](https://travis-ci.org/tmarktaylor/monotable.svg?branch=master)](https://travis-ci.org/tmarktaylor/monotable) on [Travis CI](https://travis-ci.org/)

[![Code Coverage](https://codecov.io/gh/tmarktaylor/monotable/coverage.svg?branch=master)](https://codecov.io/gh/tmarktaylor/monotable?branch=master)

[Documentation](https://monotable.readthedocs.io/en/latest/) |
[Homepage](https://github.com/tmarktaylor/monotable) |
[Build](https://travis-ci.org/tmarktaylor/monotable) |
[Codecov](https://codecov.io/gh/tmarktaylor/monotable?branch=master) |
[License](https://github.com/tmarktaylor/monotable/blob/master/LICENSE)

### Sample usage
```python

from monotable import mono

headings = ['purchased\nparrot\nheart rate', 'life\nstate']

# > is needed to right align None cell since it auto-aligns to left.
# monotable uses empty string to format the second column.
formats = ['>(none=rest).0f']
cells = [[0, 'demised'],
         [0.0, 'passed on'],
         [None, 'is no more'],
         [-1],
         [0, 'ceased to be']]

print(mono(
    headings, formats, cells,
    title='Complaint\n(registered)',

    # top guideline is equals, heading is period, bottom is omitted.
    guideline_chars='=. '))
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
