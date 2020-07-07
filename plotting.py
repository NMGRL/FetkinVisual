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
from itertools import groupby
from operator import itemgetter
import matplotlib.colors as colors
import matplotlib.cm as cmx
import matplotlib.pyplot as plt
import os

from matplotlib.backends.backend_pdf import PdfPages

from message import log


def make_dtdz(count, cfg, xs, zs, ts):
    log('making dt/dz plot')
    plt.rcParams.update(cfg.fontdict)
    plt.xlabel('X Distance Along Model Space (km)')
    plt.ylabel('dt/dz')

    dz = zs - cfg.base_elevation
    dt = ts[:len(xs)] - ts[-len(xs):]
    plt.plot(xs, dt / dz)

    save(os.path.join(cfg.output_root, 'dtdz_{}.pdf'.format(count)))


def make_section(count, cfg, xs, ys, ks):
    log('making section plot')
    plt.rcParams.update(cfg.fontdict)
    plt.xlabel('X Distance Along Model Space (km)')
    plt.ylabel('Elevation (km)')

    for ki, data in groupby(zip(xs, ys, ks), key=itemgetter(2)):
        xis, yis, kis = zip(*data)
        # plt.fill_between(xis, yis)
        plt.plot(xis, yis)

    save(os.path.join(cfg.output_root, 'section_{}.pdf'.format(count)))


def make_combined_temperature_vector(count, cfg, xs, ys, vs, vectors):
    log('making temperature+vector')
    plt.rcParams.update(cfg.fontdict)
    plt.xlabel('X Distance Along Model Space (km)')
    plt.ylabel('Elevation (km)')

    x, y, u, v = vectors.T
    plt.contourf(xs, ys, vs, levels=cfg.levels, cmap=cfg.colormap)
    add_colorbar(cfg)

    plt.quiver(x, y, u, v, color=cfg.vector_color, width=0.002)

    save(os.path.join(cfg.output_root, 'combined_temperature_vector_{}.pdf'.format(count)))


def make_combined_temperature_position(count, cfg, xs, ys, vs, sxs, sys):
    log('making temperature+position')
    plt.rcParams.update(cfg.fontdict)
    plt.xlabel('X Distance Along Model Space (km)')
    plt.ylabel('Elevation (km)')

    sxs, sys = zip(*sorted(zip(sxs, sys)))
    plt.plot(sxs, sys)
    plt.contourf(xs, ys, vs, levels=cfg.levels, cmap=cfg.colormap)

    add_colorbar(cfg)

    save(os.path.join(cfg.output_root, 'combined_temperature_position_{}.pdf'.format(count)))


def make_forward(cfg, xs, ys):
    log('making forward')
    plt.rcParams.update(cfg.fontdict)
    plt.xlabel('X Distance Along Model Space (km)')
    plt.ylabel('Age (Ma)')
    plt.title('Sample Forward')

    plt.plot(xs, ys)
    save(os.path.join(cfg.output_root, 'sample_forward.pdf'))


def make_sample_positions(count, cfg, xs, ys):
    log('making sample positions')
    plt.rcParams.update(cfg.fontdict)
    plt.xlabel('X Distance Along Model Space (km)')
    plt.ylabel('Elevation (km)')
    plt.title('Sample Position')

    xs, ys = zip(*sorted(zip(xs, ys)))
    plt.plot(xs, ys)
    save(os.path.join(cfg.output_root, 'sample_position_{}.pdf'.format(count)))


def make_topography(count, cfg, xs, ys):
    log('making topography')
    plt.rcParams.update(cfg.fontdict)
    plt.xlabel('X Distance Along Model Space (km)')
    plt.ylabel('Elevation (km)')
    plt.title('Topography')
    plt.plot(xs, ys)
    save(os.path.join(cfg.output_root, 'topography_{}.pdf'.format(count)))


def make_isotherms(count, cfg, xs, ys, vs):
    log('making isotherms')
    plt.rcParams.update(cfg.fontdict)
    plt.xlabel('X Distance Along Model Space (km)')
    plt.ylabel('Elevation (km)')
    plt.title('Isotherms (C)')
    ax = plt.contour(xs, ys, vs, levels=cfg.isotherms, colors='red')
    if cfg.label_isotherms:
        plt.clabel(ax, fmt='%0.0f (C)')

    save(os.path.join(cfg.output_root, 'isotherms_{}.pdf'.format(count)))


def make_temperature_plot(count, cfg, xs, ys, vs):
    log('making temperature')
    plt.rcParams.update(cfg.fontdict)
    plt.xlabel('X Distance Along Model Space (km)')
    plt.ylabel('Elevation (km)')
    plt.title('Temperature (C)')
    plt.contourf(xs, ys, vs, levels=cfg.levels, cmap=cfg.colormap)
    add_colorbar(cfg)
    save(os.path.join(cfg.output_root, 'temperature_{}.pdf'.format(count)))


def add_colorbar(cfg):
    bar = plt.colorbar(pad=0.01)
    bar.mappable.set_clim(cfg.colormap_min, cfg.colormap_max)
    bar.ax.invert_yaxis()
    bar.set_label('Temperature (C)')


def make_coolhistory(config, tis, tes, color, label):
    plt.plot(tis, tes, color=color, label=label)


def format_coolhistory(config):
    ax = plt.gca()
    ax.set_facecolor(config.ch['bgcolor'])
    plt.xlabel('Time (Ma)')
    plt.ylabel('Temperature (C)')
    plt.title(config.ch['title'])
    plt.legend(loc=config.ch['legend_location'])


def make_line_color_mapper(cmap, start, end):
    jet = cm = plt.get_cmap(cmap)
    cNorm = colors.Normalize(vmin=start, vmax=end)
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

    def func(v):
        return scalarMap.to_rgba(v)

    return func


def save(opath):
    plt.tight_layout()
    pp = PdfPages(opath)
    pp.savefig()
    pp.close()
    plt.clf()
# ============= EOF =============================================
