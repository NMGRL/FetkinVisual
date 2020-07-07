# ===============================================================================
# Copyright 2020 ross
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
from numpy import array

from plotting import make_coolhistory, save, make_line_color_mapper, format_coolhistory


def extract_data(path):
    data = []
    with open(path, 'r') as rfile:
        for line in rfile:
            row = line.strip().split(' ')
            ti, te = float(row[0]), float(row[-1])
            data.append((ti, te))

    return array(data).T


def coolhistory(config):
    print('doing cooling history')
    r = config.ch['range']
    print('range: {}'.format(r))

    start, end = r.split('-')
    start, end = int(start), int(end)

    func = make_line_color_mapper(config.ch['colormap'], start, end)

    for i in range(start, end + 1):
        name = '{}_tt_{}_auto_name_{}.txt'.format(config.prefix, config.ch['tag'], i)
        print(i, name)
        tis, tes = extract_data(os.path.join(config.root, name))
        make_coolhistory(config, tis, tes, func(i), i)

    format_coolhistory(config)
    save(os.path.join(config.output_root, 'ch.pdf'))
# ============= EOF =============================================
