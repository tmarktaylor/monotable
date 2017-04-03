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
# flake8: noqa    prevents all warnings, was getting F401 imported but unused

from monotable.table import MonoTable
from monotable.table import MonoTableCellError
from monotable.table import HR

from monotable.alignment import TOP
from monotable.alignment import BOTTOM
from monotable.alignment import CENTER_BOTTOM
from monotable.alignment import CENTER_TOP

__version__ = '1.0.2'
