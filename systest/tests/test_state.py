########
# Copyright (c) 2015 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
############

import unittest

from systest import conf
from systest import state


class TestState(unittest.TestCase):

    def test(self):
        obj = object()
        state.current_conf.set(obj)
        try:
            self.assertIs(obj, conf._get_current_object())
        finally:
            state.current_conf.clear()
