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


def extract_vectors(vp, cfg):
    vectors = []
    with open(vp, 'r') as rfile:
        for line in rfile:
            line = line.strip()
            line = [a.strip() for a in line.split('\t')]
            vector = [float(a) for a in line[3:]]

            x = int(vector[0])
            y = vector[1]
            if cfg.vector_every_n and x % cfg.vector_every_n:
                continue

            vectors.append(vector)

    return array(vectors)[::cfg.vector_downsample]


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

        tp = get_file(root, count, 'sample_{}'.format(cfg.sample_tag))
        sxs, sys = extract_sample_positions(tp)
        make_sample_positions(count, cfg, sxs, sys)

        if cfg.combine_temperature_position:
            make_combined_temperature_position(count, cfg, xs, ys, vs, sxs, sys)

        # todo: plot vectors on temperature plot
        if cfg.combine_temperature_vectors:
            vector_name = cfg.vector_map.get(count)
            if vector_name is not None:
                vectors = extract_vectors(os.path.join(root, '{}.dat'.format(vector_name)), cfg)
                make_combined_temperature_vector(count, cfg, xs, ys, vs, vectors)

        tp = get_file(root, count, 'topography')
        txs, tys = extract_topography(tp)
        make_topograph(count, cfg, txs, tys)

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


def make_combined_temperature_vector(count, cfg, xs, ys, vs, vectors):
    plt.xlabel('X Distance Along Model Space (km)')
    plt.ylabel('Elevation (km)')

    x, y, u, v = vectors.T
    plt.contourf(xs, ys, vs, levels=cfg.levels, cmap=cfg.colormap)
    add_colorbar(cfg)

    plt.quiver(x, y, u, v, color=cfg.vector_color, width=0.002)

    save(os.path.join(cfg.output_root, 'combined_temperature_vector_{}.pdf'.format(count)))


def make_combined_temperature_position(count, cfg, xs, ys, vs, sxs, sys):
    plt.xlabel('X Distance Along Model Space (km)')
    plt.ylabel('Elevation (km)')

    sxs, sys = zip(*sorted(zip(sxs, sys)))
    plt.plot(sxs, sys)
    plt.contourf(xs, ys, vs, levels=cfg.levels, cmap=cfg.colormap)

    add_colorbar(cfg)

    save(os.path.join(cfg.output_root, 'combined_temperature_position_{}.pdf'.format(count)))


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
    add_colorbar(cfg)
    save(os.path.join(cfg.output_root, 'temperature_{}.pdf'.format(count)))


def add_colorbar(cfg):
    bar = plt.colorbar()
    bar.mappable.set_clim(cfg.colormap_min, cfg.colormap_max)
    bar.ax.invert_yaxis()


def save(opath):
    pp = PdfPages(opath)
    pp.savefig()
    pp.close()
    plt.clf()

# ============= EOF =============================================
