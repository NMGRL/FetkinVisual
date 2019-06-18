# ===============================================================================
# Copyright 2019 ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============================================================================
import os

from argparser import parser
from config import Config
from visualization import generate_visualization


def welcome():
    print('''    
  ___    _   _  ___   __   ___              _ 
 | __|__| |_| |/ (_)_ \ \ / (_)____  _ __ _| |
 | _/ -_)  _| ' <| | ' \ V /| (_-< || / _` | |
 |_|\___|\__|_|\_\_|_||_\_/ |_/__/\_,_\__,_|_|
                                              
Developed by Jake Ross, Brandon Lutz. NMT

''')


def main():
    DEBUG = os.getenv('DEBUG')
    config = Config()
    if DEBUG:
        root = '.'
        config.output_root = '/Users/ross/Sandbox/fetkin2'
    else:
        args = parser.parse_args()
        welcome()
        root = args.root

    if root == '.':
        root = os.getcwd()
        print('Using directory={}'.format(root))
        if DEBUG:
            root = os.path.join(root, 'data', 'MuscAr_grad27')

    config.root = root
    if DEBUG:
        config_file = 'config.yaml'
    else:
        config_file = args.config
        if not config_file:
            # look for config file in root
            p = os.path.join(root, 'config.yaml')
            if os.path.isfile(p):
                if input('Config file found in directory. Would you like to use it? [y]/n>>').lower() == ['', 'y',
                                                                                                          '\n']:
                    config_file = p

    if config_file:
        config.load(config_file)
    else:
        if args.shape:
            config.shape = [int(s) for s in args.shape.split(',')]

        config.levels = args.levels
        config.sample_tag = args.sample_tag
        if args.figure_size:
            config.figure_size = [float(f) for f in args.figure_size.split(',')]

        if config.output_root is None:
            config.output_root = os.path.join(root, 'output')

    if not os.path.isdir(config.output_root):
        os.mkdir(config.output_root)

    generate_visualization(config)


if __name__ == '__main__':
    main()

# ============= EOF =============================================
