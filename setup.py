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

from setuptools import setup


setup(
    name='claw',
    version='0.1',
    author='GigaSpaces',
    author_email='cosmo-admin@gigaspaces.com',
    packages=['claw',
              'claw.handlers',
              'claw.resources'],
    description='Cloudify Almighty Wrapper',
    license='Apache License, Version 2.0',
    zip_safe=False,
    install_requires=[
        'cloudify-system-tests',
        'argcomplete',
        'argh',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'claw = claw.main:main',
        ],
    }
)
