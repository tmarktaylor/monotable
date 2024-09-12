# monotable ASCII table formatter.
#
# Copyright 2020, 2024 Mark Taylor
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

"""ASCII table: per column format specs, formatting directives, multi-line.
"""
__version__ = '3.2.0'

__all__ = ['HR_ROW', 'VR_COL', 'mono', 'monocol', 'join_strings', 'MonoTable']

from monotable.datacls import dataclass_format
from monotable.datacls import dataclass_print
from monotable.datacls import stow
from monotable.mono import HR_ROW
from monotable.mono import VR_COL
from monotable.mono import mono
from monotable.mono import monocol
from monotable.mono import join_strings
from monotable.table import MonoTable
