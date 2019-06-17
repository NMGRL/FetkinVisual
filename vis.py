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


def welcome():
    print('''    
 _______  _______  _______  ___   _  ___   __    _  __   __  ___   _______  __   __  _______  ___     
|       ||       ||       ||   | | ||   | |  |  | ||  | |  ||   | |       ||  | |  ||   _   ||   |    
|    ___||    ___||_     _||   |_| ||   | |   |_| ||  |_|  ||   | |  _____||  | |  ||  |_|  ||   |    
|   |___ |   |___   |   |  |      _||   | |       ||       ||   | | |_____ |  |_|  ||       ||   |    
|    ___||    ___|  |   |  |     |_ |   | |  _    ||       ||   | |_____  ||       ||       ||   |___ 
|   |    |   |___   |   |  |    _  ||   | | | |   | |     | |   |  _____| ||       ||   _   ||       |
|___|    |_______|  |___|  |___| |_||___| |_|  |__|  |___|  |___| |_______||_______||__| |__||_______|


Developed by Jake Ross, Brandon Lutz. NMT

''')

def main():
    args = parser.parse_args()

    welcome()

    root = args.root
    if root == '.':
        root = os.getcwd()
        print('Using directory={}'.format(root))




if __name__ == '__main__':
    main()

# ============= EOF =============================================
