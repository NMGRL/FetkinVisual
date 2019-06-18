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
import glob
import os

from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from numpy import meshgrid, array


def list_files(root, tag):
    name = os.path.basename(root)
    pathname = os.path.join(root, '{}_{}_*.txt'.format(name, tag))
    print('pathname={}'.format(pathname))
    return sorted(glob.glob(pathname))


def get_file(root, count, tag):
    name = '{}_{}_{}.txt'.format(os.path.basename(root), tag, count)
    return os.path.join(root, name)


def extract_values(p):
    vs = []
    with open(p, 'r') as rfile:
        for line in rfile:
            vs.append(float(line.strip()))
    return array(vs)


def extract_xy(np, skip=0, idxs=None):
    delimiter = ' '
    xs, ys = [], []
    if idxs is None:
        idxs = [0, -1]

    with open(np, 'r') as rfile:
        for i in range(skip):
            next(rfile)

        for line in rfile:
            line = line.strip()
            args = line.split(delimiter)
            args = [a for a in args if a != '']

            xs.append(float(args[idxs[0]]))
            ys.append(float(args[idxs[1]]))

    return array(xs), array(ys)


def extract_topography(tp):
    return extract_xy(tp, skip=1)


def extract_nodes(np):
    return extract_xy(np)


def extract_sample_positions(sp):
    return extract_xy(sp, idxs=[0, 1])


def extract_sample_forward(fp):
    return extract_xy(fp, idxs=[0, 1])


def generate_visualization(cfg):
    # get the file counters

    root = cfg.root
    counters = []
    for p in list_files(root, 'values'):
        name = os.path.basename(p).split('.')[0]
        count = name.split('_')[-1]
        counters.append(count)

    plt.figure(figsize=cfg.figure_size)
    for count in counters:
        vp = get_file(root, count, 'values')
        vs = extract_values(vp)
        np = get_file(root, count, 'nodes')
        xs, ys = extract_nodes(np)

        xs, ys, vs = prep(cfg, xs, ys, vs)
        make_temperature_plot(count, cfg, xs, ys, vs)
        make_isotherms(count, cfg, xs, ys, vs)

        tp = get_file(root, count, 'topography')
        xs, ys = extract_topography(tp)
        make_topograph(count, cfg, xs, ys)

        tp = get_file(root, count, 'sample_{}'.format(cfg.sample_tag))
        xs, ys = extract_sample_positions(tp)
        make_sample_positions(count, cfg, xs, ys)
        break

    fp = get_file(root, cfg.sample_tag, 'sample_forward')
    xs, ys = extract_sample_forward(fp)
    make_forward(cfg, xs, ys)


def prep(cfg, xs, ys, vs):
    xs = array(xs)
    ys = array(ys)
    vs = array(vs)

    xs = xs.reshape(cfg.shape)
    ys = ys.reshape(cfg.shape)
    vs = vs.reshape(cfg.shape)
    return xs, ys, vs


def make_forward(cfg, xs, ys):
    plt.xlabel('X Distance Along Model Space (km)')
    plt.ylabel('Age (Ma)')
    plt.title('Sample Forward')

    plt.plot(xs, ys)
    save(os.path.join(cfg.output_root, 'sample_forward.pdf'))


def make_sample_positions(count, cfg, xs, ys):
    plt.xlabel('X Distance Along Model Space (km)')
    plt.ylabel('Elevation (km)')
    plt.title('Sample Position')

    xs, ys = zip(*sorted(zip(xs, ys)))
    plt.plot(xs, ys)
    save(os.path.join(cfg.output_root, 'sample_position_{}.pdf'.format(count)))


def make_topograph(count, cfg, xs, ys):
    plt.xlabel('X Distance Along Model Space (km)')
    plt.ylabel('Elevation (km)')
    plt.title('Topography')
    plt.plot(xs, ys)
    save(os.path.join(cfg.output_root, 'topography_{}.pdf'.format(count)))


def make_isotherms(count, cfg, xs, ys, vs):
    plt.xlabel('X Distance Along Model Space (km)')
    plt.ylabel('Elevation (km)')
    plt.title('Isotherms (C)')
    plt.contour(xs, ys, vs, levels=cfg.isotherms, colors='red')
    save(os.path.join(cfg.output_root, 'isotherms_{}.pdf'.format(count)))


def make_temperature_plot(count, cfg, xs, ys, vs):
    plt.xlabel('X Distance Along Model Space (km)')
    plt.ylabel('Elevation (km)')
    plt.title('Temperature (C)')
    plt.contourf(xs, ys, vs, levels=cfg.levels, cmap=cfg.colormap)
    plt.colorbar()
    save(os.path.join(cfg.output_root, 'temperature_{}.pdf'.format(count)))


def save(opath):
    pp = PdfPages(opath)
    pp.savefig()
    pp.close()
    plt.clf()

# ============= EOF =============================================
