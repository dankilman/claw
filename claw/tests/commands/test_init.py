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

import sh

from claw import resources
from claw import tests


class InitTest(tests.BaseTest):

    def test_basic(self, reset=False):
        with self.workdir:
            self.claw.init(reset=reset)
        self._verify_init(expected_claw_home=self.workdir,
                          expected_suites_yaml=self.main_suites_yaml_path)

    def test_settings_exists_no_reset(self):
        self.test_basic()
        with self.assertRaises(sh.ErrorReturnCode):
            self.test_basic()

    def test_settings_exists_reset(self):
        self.test_basic()
        self.test_basic(reset=True)

    def test_explicit_suites_yaml(self):
        suites_yaml = self.workdir / 'main-suites.yaml'
        suites_yaml.touch()
        with self.workdir:
            self.claw.init(suites_yaml=suites_yaml)
        self._verify_init(expected_claw_home=self.workdir,
                          expected_suites_yaml=suites_yaml)

    def test_suites_yaml_does_not_exist(self):
        with self.workdir:
            # sanity
            self.claw.init(suites_yaml=self.main_suites_yaml_path)
            with self.assertRaises(sh.ErrorReturnCode):
                self.claw.init(
                    suites_yaml='some_path_that_does_not_exist.yaml')

    def test_explicit_claw_home(self):
        claw_home = self.workdir / 'claw-home'
        claw_home.mkdir()
        with self.workdir:
            self.claw.init(suites_yaml=self.main_suites_yaml_path,
                           claw_home=claw_home)
        self._verify_init(expected_claw_home=claw_home,
                          expected_suites_yaml=self.main_suites_yaml_path)

    def _verify_init(self,
                     expected_claw_home,
                     expected_suites_yaml):
        self.assertTrue(self.settings.settings_path.exists())
        self.assertEqual(self.settings.claw_home, expected_claw_home)
        self.assertEqual(self.settings.main_suites_yaml, expected_suites_yaml)
        self.assertEqual(self.settings.user_suites_yaml.text(),
                         resources.get('templates/suites.template.yaml'))
        self.assertEqual(self.settings.blueprints_yaml.text(),
                         resources.get('templates/blueprints.template.yaml'))
        self.assertEqual((self.settings.claw_home / '.gitignore').text(),
                         resources.get('templates/gitignore.template'))
        self.assertEqual(
            (self.settings.default_scripts_dir / 'example-script.py').text(),
            resources.get('templates/script.template.py'))
        self.assertTrue(self.settings.configurations.exists())
