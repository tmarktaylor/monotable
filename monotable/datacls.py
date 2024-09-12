# monotable ASCII table formatter.
#
# Copyright 2024 Mark Taylor
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This file is part of Project monotable.

"""Dataclass printer. Tools to pretty print dataclasses"""

import dataclasses
import textwrap
from typing import Any, Dict, List, Optional, Tuple

import monotable


def dataclass_print(
    dataclass_instance: Any,
    *,
    max_depth: Optional[int] = None,
    # note- These 2 keyword args are monotable positional args.
    formats: Tuple[str, str] = ("", ">"),
    title: str = "",  # monotable title prefix
    **monotable_kwargs: Any,  # keyword args passed to monotable.mono().
) -> None:
    """Print the dataclass in table form in two columns: name, value.

    Dataclass field values are converted to strings and right justified.

    Dataclass members with these field metadata keys have special meaning:
    "help":  The value is printed after the member name in the name column.

    "spec":  The string value becomes a string format spec for the value.
    It is used in a replacement field in an f-string format string.

    "spec":  If a callable, the function is called with the value.
    The string returned is printed in the value column.

    If a field value is a dataclass that has metadata "spec" that is
    a callable, the function is called to format the value.

    If a field value is a dataclass with no metadata "spec" (or
    metadata spec that is not callable) a new table is
    printed below the current one. Its title will have a dotted field name.
    Any given id(dataclass_instance) will only be printed once.
    The value "..." indicates not printing an already printed dataclass.
    This breaks a possible circular reference cycle.

    Args:
        dataclass_instance

    Keyword Args:
        max_depth
            Print nested dataclasses this many levels deep. None means
            print all nested dataclasses.

        formats
            Described by the same named monotable.mono() positional arg.

        title
            String prepended to the classname in the title.
            Described by the same named monotable.mono() positional arg.

        monotable_kwargs
            These args are passed through to monotable.mono().
    """

    print(
        _format(
            dataclass_instance,
            max_depth=max_depth,
            formats=formats,
            title=title,
            **monotable_kwargs,
        )
    )


def dataclass_format(
    dataclass_instance: Any,
    *,
    max_depth: Optional[int] = None,
    # note- These 2 keyword args are monotable positional args.
    formats: Tuple[str, str] = ("", ">"),
    title: str = "",  # monotable title prefix
    **monotable_kwargs: Any,  # keyword args passed to monotable.mono().
) -> str:
    """Format a dataclass in table form in two columns: name, value.
    See dataclassprint() above for details.

    Args:
        dataclass_instance

    Keyword Args:
        max_depth
            Print nested dataclasses this many levels deep. None means
            print all nested dataclasses.

        formats
            Described by the same named monotable.mono() positional arg.

        title
            String prepended to the classname in the title.
            Described by the same named monotable.mono() positional arg.

        monotable_kwargs
            These args are passed through to monotable.mono().

    Returns:
        The text table as a single string.
    """
    return _format(
        dataclass_instance,
        max_depth=max_depth,
        formats=formats,
        title=title,
        **monotable_kwargs,
    )


def _format(
    dataclass_instance: Any,
    *,
    field_name: str = "",
    max_depth: Optional[int] = None,
    title: str = "",
    depth: int = 0,
    visited: Optional[List[int]] = None,
    **monotable_kwargs: Any,
) -> str:
    """Format a dataclass for printing. Format nested dataclasses."""
    # See dataclass_print() above for description of the shared args.
    # These are new args:
    # field_name: string prepended to a nested dataclass header.
    # visited: id(s) of dataclasses that have already been printed.
    # depth: > 1 indicates this field is a field of an enclosing dataclass.
    assert dataclasses.is_dataclass(dataclass_instance), "Must be a dataclass instance."

    # Save the Python built in function id() of the caller's
    # dataclass_instance to check later.
    if visited is None:
        visited = [id(dataclass_instance)]
    else:
        visited.append(id(dataclass_instance))
    dataclass_type = dataclass_instance.__class__.__name__
    nested_dataclasses = []
    rows = []
    left_column_width = 0

    # Add one row for each field in the dataclass instance.
    for field_info in dataclasses.fields(dataclass_instance):
        metadata_settings = unstow(field_info.metadata)
        # If help text for name is configured, append it after the name.
        help_string = metadata_settings.get("help", "")
        left_column_string = make_name_string(field_info.name, help_string)
        left_column_width = max(left_column_width, len(left_column_string))
        value = getattr(dataclass_instance, field_info.name)
        spec = metadata_settings.get("spec", "")
        # If the value is a dataclass and it has a callable spec,
        # call the function to do the formatting.
        if dataclasses.is_dataclass(value) and callable(spec):
            cell = spec(value)
        else:
            # If the value is a dataclass save it for processing later and
            # display its type as the value.
            if dataclasses.is_dataclass(value):
                dotted_field_name = make_dotted_field_name(
                    field_name, dataclass_type, field_info.name
                )
                # Avoid recursing into an already printed dataclass.
                if id(value) in visited:
                    cell = f"{dataclass_type} ..."
                else:
                    if max_depth is None or depth < (max_depth - 1):
                        # Save nested dataclass to print later.
                        nested_dataclasses.append(
                            (dotted_field_name, help_string, value)
                        )
                    # Print the class name instead of the value.
                    cell = value.__class__.__name__
            else:
                # Format the value using callers function or the format spec
                if callable(spec):
                    cell = spec(value)
                else:
                    cell = f"{value:{spec}}"

        rows.append([left_column_string, cell])

    title_string = make_title_string(title, dataclass_type)

    formatted_dataclasses = []
    table = monotable.mono(
        cellgrid=rows,
        title=title_string,
        **monotable_kwargs,
    )

    formatted_dataclasses.append(table)

    # Format the dataclasses from the list nested_dataclasses.
    # Note this is a recursive call to dataclass_format().
    # The title is the type of the outer most dataclass.
    # A dotted path shows the field names of the parent data classes.
    # The title ends with the optional field help text if the
    # field of the parent data class configured the "help" key in
    # its metadata.
    depth = depth + 1
    formatted_nested_dataclasses = do_nested(
        visited=visited,
        depth=depth,
        monotable_kwargs=monotable_kwargs,
        nested_dataclasses=nested_dataclasses,
        max_depth=max_depth,
    )
    formatted_dataclasses.extend(formatted_nested_dataclasses)
    return "\n\n".join(formatted_dataclasses)


def make_name_string(field_name: str, help_string: str) -> str:
    """Create a left justified string from field name and help text."""
    if help_string:
        name_string = f"{field_name}  {help_string}"
    else:
        name_string = field_name
    return name_string


def make_dotted_field_name(
    nested_dotted_field_name: str, dataclass_type: str, field_name: str
) -> str:
    """Return dotted fielname used for title of the nested dataclass ASCII table."""
    if nested_dotted_field_name:
        dotted_field_name = f"{nested_dotted_field_name}.{field_name}"
    else:
        dotted_field_name = f"{dataclass_type}.{field_name}"
    return dotted_field_name


def make_title_string(title: str, dataclass_type: str) -> str:
    """Return string used for title of top level ASCII table."""
    if title:
        title_string = title + " : " + dataclass_type
    else:
        title_string = dataclass_type
    return title_string


def do_nested(
    visited: List[int],
    depth: int,
    monotable_kwargs: Any,
    nested_dataclasses: List[Tuple[str, str, Any]],
    max_depth: Optional[int] = None,
) -> List[str]:
    """Format all the nested dataclasses at this depth as additional ASCII tables."""
    formatted_dataclasses: List[str] = []
    # Indent the next nested level 2 more spaces.
    # Indenting only applies to nested dataclasses.
    # We do nested dataclasses depth first.
    # When no more depth we indent 2 spaces at the lowest level and then return the
    # table string.  As we complete each recursive call an additional 2 spaces of
    # indent is applied.
    indent = "  "
    for nested_dotted_field_name, nested_help, nested in nested_dataclasses:
        nested_title = ""
        nested_title += f"{nested_dotted_field_name}"
        if nested_help:
            nested_title += f"  {nested_help}"

        table = dataclass_format(
            dataclass_instance=nested,
            max_depth=max_depth,
            field_name=nested_dotted_field_name,
            visited=visited,
            depth=depth,
            title=nested_title,
            **monotable_kwargs,
        )
        unindented_table = textwrap.indent(table, indent)
        formatted_dataclasses.append(unindented_table)
    return formatted_dataclasses


def stow(**kwargs: Any) -> Dict[str, Any]:
    """Return dict to assign to a dataclass field metadata.

    Keyword Args:
        spec
            The string value becomes a string format spec for the value.
            If a callable, the function is called with the value.

        help
            The value is printed after the member name in the name column.

    Returns:
        A dict with key "monotable" whose value is a dict contains the
        stow() keyword args.
    """

    return dict(monotable=kwargs)


def unstow(metadata: Any) -> Dict[str, Any]:
    """Return the monotable dict from dataclass field metadata."""
    field_metadata_dict: dict[str, Any] = metadata.get("monotable", dict())
    return field_metadata_dict
