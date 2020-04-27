# monotable ASCII table formatter.
#
# Copyright 2019 Mark Taylor
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
__version__ = '3.0.0'

__all__ = ['HR_ROW', 'VR_COL', 'mono', 'monocol', 'MonoTable']

from .mono import HR_ROW
from .mono import VR_COL
from .mono import mono
from .mono import monocol
from .table import MonoTable
