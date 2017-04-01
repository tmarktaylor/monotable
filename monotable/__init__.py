# monotable ASCII table formatter.
#
# Copyright 2017 Mark Taylor
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

"""ASCII table: per column format specs, plug-in format functions, multi-line.
"""
# The # noqa: F401 prevents flake8 F401 imported but unused warnings

from monotable.table import MonoTable    # noqa: F401
from monotable.table import MonoTableCellError    # noqa: F401
from monotable.table import HR    # noqa: F401

from monotable.alignment import TOP    # noqa: F401
from monotable.alignment import BOTTOM    # noqa: F401
from monotable.alignment import CENTER_BOTTOM    # noqa: F401
from monotable.alignment import CENTER_TOP    # noqa: F401

__version__ = '1.0.1'
