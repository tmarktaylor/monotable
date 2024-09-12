# monotable

ASCII table with per column format specs, multi-line content,
formatting directives, column width control.

Dataclass to ASCII table printer.

## default branch status

[![](https://img.shields.io/pypi/l/monotable.svg)](http://www.apache.org/licenses/LICENSE-2.0)
[![](https://img.shields.io/pypi/v/monotable.svg)](https://pypi.python.org/pypi/monotable)
[![](https://img.shields.io/pypi/pyversions/monotable.svg)](https://pypi.python.org/pypi/monotable)

[![CI Test](https://github.com/tmarktaylor/monotable/actions/workflows/ci.yml/badge.svg)](https://github.com/tmarktaylor/monotable/actions/workflows/ci.yml)
[![readthedocs](https://readthedocs.org/projects/monotable/badge/?version=latest)](https://monotable.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/tmarktaylor/monotable/branch/master/graph/badge.svg?token=qanSaWfGAQ)](https://codecov.io/gh/tmarktaylor/monotable)

[Docs](https://monotable.readthedocs.io/en/latest/) |
[Repos](https://github.com/tmarktaylor/monotable) |
[Codecov](https://codecov.io/gh/tmarktaylor/monotable?branch=master) |
[License](https://github.com/tmarktaylor/monotable/blob/master/LICENSE)

## Sample usage

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

```expected-output
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

## Dataclass to ASCII Table printer

```python
from dataclasses import dataclass, field
from enum import auto, Enum
from monotable import dataclass_print
from monotable import dataclass_format
from monotable import stow
```

### Print a dataclass instance

Print a dataclass as an ASCII table. The field names are left
justified in the left column. The values are right justified
in the right column.

```python
@dataclass
class CurrentConditions:
    temperature: float
    humidity: float
    heat_index: int

weather_data = CurrentConditions(80.0, 0.71, 83)
dataclass_print(weather_data)
```

```expected-output
CurrentConditions
-----------------
temperature  80.0
humidity     0.71
heat_index     83
-----------------
```

### Title

The table title defaults to the class name. The string passed
to the "title" keyword is prepended to the class name.

```python
dataclass_print(weather_data, title="Airport")
```

```expected-output
Airport : CurrentConditions
-----------------
temperature  80.0
humidity     0.71
heat_index     83
-----------------
```

### Format and print later

Call dataclass_format() to print or log later.

```python
text = dataclass_format(weather_data, title="Airport")
print(text)
```

```expected-output
Airport : CurrentConditions
-----------------
temperature  80.0
humidity     0.71
heat_index     83
-----------------
```

### Add a format spec to a dataclass field

Specify formatting for a data class field as shown for
the field() call in place of the default value for the
humidity field below.

The function stow() assigns the dict {"spec": ".0%"} to
the field's metadata dict as the value for the key
"monotable".
The code internally applies this f-string: f"{value:{spec}}"
to format the value.

```python
@dataclass
class SpecCurrentConditions:
    temperature: float
    humidity: float = field(metadata=stow(spec=".0%"))
    heat_index: int

weather_data = SpecCurrentConditions(80.0, 0.71, 83)
dataclass_print(weather_data)
```

```expected-output
SpecCurrentConditions
-----------------
temperature  80.0
humidity      71%
heat_index     83
-----------------
```

### Add a format function to a dataclass field

Specify a format function to do the formatting for a field.

Set the 'spec' key to a callable.
The function takes the field value as the parameter and returns a string.
The string is printed in the table. Note that just the enumeration
name "E" is printed instead of "Direction.E".

```python
class Direction(Enum):
    N = auto()
    E = auto()
    S = auto()
    W = auto()


@dataclass
class Wind:
    speed: int
    direction: Direction = field(metadata=stow(spec=lambda x: x.name))

wind_data = Wind(speed=11,direction=Direction.E)
dataclass_print(wind_data)
```

```expected-output
     Wind
-------------
speed      11
direction   E
-------------
```

### Add text to embellish a field name

Set the 'help' key to add text immediately after the field name.
This is printed in the table left column:
- dataclass field name
- 2 spaces
- 'help' key value.

```python
@dataclass
class MoreConditions:
    visibility: float = field(metadata=stow(help="(mi)",spec=".2f"))
    dewpoint: int = field(metadata=stow(help="(degF)"))

more_data = MoreConditions(visibility=10.00,dewpoint=71)
dataclass_print(more_data)
```

```expected-output
     MoreConditions
-----------------------
visibility  (mi)  10.00
dewpoint  (degF)     71
-----------------------
```

### When a dataclass field value is also dataclass

An additional ASCII table is printed for each nested dataclass.
The table is below and indented two spaces for each level of nesting.

```python
@dataclass
class MoreCurrentConditions:
    temperature: float
    humidity: float
    heat_index: int
    wind: Wind = field(metadata=stow(help="(2pm)"))

more_weather_data = MoreCurrentConditions(
    80.0, 0.71, 83, Wind(11, Direction.E)
    )
dataclass_print(more_weather_data)
```

The class name is printed in place of the value. The value of
the wind field is printed in a second table below the first
and indented two spaces.

```expected-output
MoreCurrentConditions
-----------------
temperature  80.0
humidity     0.71
heat_index     83
wind  (2pm)  Wind
-----------------

  MoreCurrentConditions.wind  (2pm) : Wind
  -------------
  speed      11
  direction   E
  -------------
```

#### Omit printing a nested dataclass

To prevent levels of nested dataclasses from printing pass
keyword parameter max_depth. 1 means just print the top
level of dataclass. Note that only the classname of
the wind field value is printed.

```python
dataclass_print(more_weather_data, max_depth=1)
```

```expected-output
MoreCurrentConditions
-----------------
temperature  80.0
humidity     0.71
heat_index     83
wind  (2pm)  Wind
-----------------
```


#### Print a bordered ASCII table

dataclass_print() passes extra keyword arguments to monotable.mono().
See monotable.mono()'s documentation. Some examples are below.

```python
dataclass_print(more_weather_data, max_depth=1, bordered=True)
```

```expected-output
MoreCurrentConditions
+-------------+------+
| temperature | 80.0 |
+-------------+------+
| humidity    | 0.71 |
+-------------+------+
| heat_index  |   83 |
+-------------+------+
| wind  (2pm) | Wind |
+-------------+------+
```

#### Print ASCII table with indent

```python
dataclass_print(more_weather_data, max_depth=1, indent="....")
```

```expected-output
....MoreCurrentConditions
....-----------------
....temperature  80.0
....humidity     0.71
....heat_index     83
....wind  (2pm)  Wind
....-----------------
```

#### Change the column alignment

```python
dataclass_print(more_weather_data, max_depth=1, formats=(">", "<"))
```

```expected-output
MoreCurrentConditions
-----------------
temperature  80.0
   humidity  0.71
 heat_index  83
wind  (2pm)  Wind
-----------------
```

#### Print a nested dataclass that has a callable spec

For a dataclass field value, set the monotable field metadata
"spec" key to a function so that the value is printed in the top
level table rather than below as a separate table.

Note- This example is coded in Python REPL style so it can be tested
by the PYPI project phmutest using --replmode.

```python
>>> from dataclasses import dataclass, field
>>> from enum import auto, Enum
>>>
>>> from monotable import dataclass_print
>>> from monotable import stow
>>>
>>> class Direction(Enum):
...     N = auto()
...     E = auto()
...     S = auto()
...     W = auto()
>>>
>>> @dataclass
... class Wind:
...     speed: int
...     direction: Direction = field(metadata=stow(spec=lambda x: x.name))
>>>
>>> @dataclass
... class WindInline:
...     temperature: float
...     humidity: float
...     heat_index: int
...     wind: Wind = field(metadata=stow(spec=str))

>>> wind = Wind(11, Direction.E)
>>> wind_inline = WindInline(80.0, 0.71, 83, wind)
>>> dataclass_print(wind_inline)
                       WindInline
-------------------------------------------------------
temperature                                        80.0
humidity                                           0.71
heat_index                                           83
wind         Wind(speed=11, direction=<Direction.E: 2>)
-------------------------------------------------------
```

#### Left align the title

Note "<" at the start of title= specifies left alignment.
monotable detects alignment from the first character of the title.

```python
>>> dataclass_print(wind_inline, title="<Left Aligned Title")
Left Aligned Title : WindInline
-------------------------------------------------------
temperature                                        80.0
humidity                                           0.71
heat_index                                           83
wind         Wind(speed=11, direction=<Direction.E: 2>)
-------------------------------------------------------
```

#### Recipe to do dataclass_print as a mixin class.

```python
from typing import Any, Tuple

class DCPrint:
    """Mixin class for dataclass to add member function dcprint()."""

    # This should be the same signature as dataclass_print()
    # where dataclass_instance is replaced by self.
    def dcprint(
        self,
        *,
        # note- These 2 keyword args are monotable positional args.
        formats: Tuple[str, str] = ("", ">"),
        title: str = "",  # monotable title prefix
        **monotable_kwargs: Any,  # keyword args passed to monotable.mono().
    ) -> None:

        dataclass_print(
            self,
            formats=formats,
            title=title,
            **monotable_kwargs,
        )
```

Add DCPrint as a base class to the dataclass definition.

```python
@dataclass
class Temperatures(DCPrint):
    high: int
    low: int

temps = Temperatures(high=77, low=60)
temps.dcprint(title="High/Low Temperature")
```

```expected-output
High/Low Temperature : Temperatures
--------
high  77
low   60
--------
```
