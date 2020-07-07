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
import matplotlib.pyplot as plt
from extract import extract_values, extract_nodes, extract_sample_positions, extract_vectors, extract_topography, \
    extract_sample_forward, extract_sections
from message import warning
from pathutil import list_files, get_file
from plotting import make_temperature_plot, make_isotherms, make_sample_positions, make_combined_temperature_position, \
    make_combined_temperature_vector, make_topography, make_forward, make_section, make_dtdz


def generate_visualization(cfg):
    # get the file counters

    root = cfg.root
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
    for count in counters:
        print('Time step: {}'.format(count))

        sp = get_file(cfg, count, 'section')
        if sp:
            sxs, sys, sks = extract_sections(sp)
            make_section(count, cfg, sxs, sys, sks)

        vp = get_file(cfg, count, 'values')
        hastemp = False
        if vp:
            vs = extract_values(vp)

            np = get_file(cfg, count, 'nodes')
            if np:
                xs, ys = extract_nodes(np)

                xs = xs.reshape(cfg.shape)
                ys = ys.reshape(cfg.shape)
                vs = vs.reshape(cfg.shape)

                hastemp = True

        if hastemp:
            make_temperature_plot(count, cfg, xs, ys, vs)
            make_isotherms(count, cfg, xs, ys, vs)
        else:
            warning('No Temperature data')

        hasposition = False
        tp = get_file(cfg, count, 'sample_{}'.format(cfg.sample_tag))
        if tp:
            sxs, sys = extract_sample_positions(tp)
            make_sample_positions(count, cfg, sxs, sys)
            hasposition = True

        if hasposition:
            if cfg.combine_temperature_position:
                make_combined_temperature_position(count, cfg, xs, ys, vs, sxs, sys)
        else:
            warning('No Sample Position data')

        if hastemp:
            if cfg.combine_temperature_vectors:
                vector_name = cfg.vector_map.get(count)
                if vector_name is not None:
                    vp = os.path.join(root, '{}.dat'.format(vector_name))
                    if os.path.isfile(vp):
                        vectors = extract_vectors(vp, cfg)
                        make_combined_temperature_vector(count, cfg, xs, ys, vs, vectors)
                    else:
                        print('Does not exist: "{}"'.format(vp))
                        warning('No vector file for {} - {}'.format(count, vector_name))

        tp = get_file(cfg, count, 'topography')
        if tp:
            txs, tys = extract_topography(tp)
            make_topography(count, cfg, txs, tys)
            vp = get_file(cfg, count, 'values')
            if vp:
                vs = extract_values(vp)
                make_dtdz(count, cfg, txs, tys, vs)
                continue
        else:
            warning('No Topography data')

        if int(os.getenv('DEBUG', 0)):
            break

    fp = get_file(cfg, cfg.sample_tag, 'sample_forward')
    if fp:
        xs, ys = extract_sample_forward(fp)
        make_forward(cfg, xs, ys)
    else:
        warning('No sample forward data')


# ============= EOF =============================================
