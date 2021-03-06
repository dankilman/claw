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

from claw import tests
from claw import patcher
from claw import configuration


class CleanupTest(tests.BaseTestWithInit):

    def setUp(self):
        super(CleanupTest, self).setUp()
        with patcher.YamlPatcher(self.settings.user_suites_yaml) as patch:
            obj = patch.obj
            conf = obj['handler_configurations'][tests.STUB_CONFIGURATION]
            conf['handler'] = 'stub_handler'
        self.configuration = configuration.Configuration(
            tests.STUB_CONFIGURATION)

    def test_basic(self):
        self.claw.generate(tests.STUB_CONFIGURATION)
        output = self.claw.cleanup(tests.STUB_CONFIGURATION).stdout.strip()
        self.assertIn('Stub handler cleanup', output)
        self.assertTrue(self.configuration.exists())
        self.assertTrue((self.settings.configurations /
                         configuration.CURRENT_CONFIGURATION).islink())

    def test_no_configuration(self):
        output = self.claw.cleanup(tests.STUB_CONFIGURATION).stdout.strip()
        self.assertIn('Stub handler cleanup', output)
        self.assertFalse(self.configuration.exists())
        self.assertFalse((self.settings.configurations /
                          configuration.CURRENT_CONFIGURATION).islink())
