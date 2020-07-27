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
import matplotlib.pyplot as plt
from numpy import arange
import os

from extract import extract_values
from pathutil import get_file, list_files
from plotting import save


def dtdz(cfg):
    counters = []
    for p in list_files(cfg, 'values'):
        name = os.path.basename(p).split('.')[0]
        count = name.split('_')[-1]
        counters.append(count)

    figsize = cfg.figure_size
    if figsize is None:
        h, w = cfg.shape
        figsize = (w / 10, h / 10 * cfg.vertical_exaggeration)

    plt.figure(figsize=figsize)
    print('config output: {}'.format(cfg.output_root))

    _, ncols = cfg.shape
    for count in counters:
        vp = get_file(cfg, count, 'values')
        if vp:
            vs = extract_values(vp)
            xs = arange(ncols)
            plt.rcParams.update(cfg.fontdict)
            plt.xlabel('X Distance Along Model Space (km)')
            plt.ylabel('Geothermal Gradient (C/km)')

            vs = vs[::-1]

            d0 = cfg.dtdz['depth_start']
            d1 = cfg.dtdz['depth_end']

            dt0 = vs[d0 * ncols:(d0 + 1) * ncols]
            dt1 = vs[d1 * ncols:(d1 + 1) * ncols]

            try:
                dt = dt1 - dt0
                dz = 1

                plt.plot(xs, cfg.dtdz['thermal_conductivity'] * dt[::-1] / dz)
            except ValueError:
                pass

            # plt.show()
            save(os.path.join(cfg.output_root, 'heatflow_{}.pdf'.format(count)))
# ============= EOF =============================================
