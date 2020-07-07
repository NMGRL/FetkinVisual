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
import sys

from config import Config
from message import warning

from visualization import generate_visualization
from ch import coolhistory


def welcome():
    print('''    
  ___    _   _  ___   __   ___              _ 
 | __|__| |_| |/ (_)_ \ \ / (_)____  _ __ _| |
 | _/ -_)  _| ' <| | ' \ V /| (_-< || / _` | |
 |_|\___|\__|_|\_\_|_||_\_/ |_/__/\_,_\__,_|_|
                                              
Developed by Jake Ross, Brandon Lutz. NMT 2019

''')


COMMANDS = {'plot': generate_visualization,
            'ch': coolhistory}

def main():
    DEBUG = int(os.getenv('DEBUG', 0))
    config = Config()
    if DEBUG:
        root = '.'
        config.output_root = '/Users/ross/Sandbox/fetkin2'
    else:
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('command')
        parser.add_argument('root', metavar='root')
        parser.add_argument('--config', metavar='config')
        args = parser.parse_args()
        welcome()
        root = args.root

    if root == '.':
        root = os.getcwd()
        print('Using directory={}'.format(root))
        if DEBUG:
            root = os.path.join(root, 'data', 'Zhe_40_prop1')

    config.root = root
    if DEBUG:
        config_file = 'config.yaml'
    else:
        config_file = args.config
        if not config_file:
            # look for config file in root
            p = os.path.join(root, 'config.yaml')
            if os.path.isfile(p):
                if input('Config file found in directory. '
                         'Would you like to use it? [y]/n>>').lower() in ['', 'y', '\n', '\r\n', '\r']:
                    config_file = p

    if config_file and os.path.isfile(config_file):
        config.load(config_file)
    else:
        warning('Could not locate a config file')
        sys.exit(1)

    if config.output_root is None:
        config.output_root = os.path.join(root, 'visualizations')

    if config.use_unique_output_root:
        oroot = config.output_root
        dirname = os.path.dirname(oroot)
        base = os.path.basename(oroot)
        counter = 0
        while os.path.isdir(oroot):
            oroot = os.path.join(dirname, '{}{:04d}'.format(base, counter))
            counter += 1

        config.output_root = oroot

    if not os.path.isdir(config.output_root):
        os.mkdir(config.output_root)

    try:
        COMMANDS[args.command](config)
    except KeyError as e:
        warning('invalid command={}. valid COMMANDS={}'.format(args.command, COMMANDS.keys()))
        warning(e)

if __name__ == '__main__':
    main()

# ============= EOF =============================================
