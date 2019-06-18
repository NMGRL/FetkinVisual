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
import matplotlib.pyplot as plt
import os

from matplotlib.backends.backend_pdf import PdfPages

from message import log


def make_combined_temperature_vector(count, cfg, xs, ys, vs, vectors):
    log('making temperature+vector')

    plt.xlabel('X Distance Along Model Space (km)')
    plt.ylabel('Elevation (km)')

    x, y, u, v = vectors.T
    plt.contourf(xs, ys, vs, levels=cfg.levels, cmap=cfg.colormap)
    add_colorbar(cfg)

    plt.quiver(x, y, u, v, color=cfg.vector_color, width=0.002)

    save(os.path.join(cfg.output_root, 'combined_temperature_vector_{}.pdf'.format(count)))


def make_combined_temperature_position(count, cfg, xs, ys, vs, sxs, sys):
    log('making temperature+position')

    plt.xlabel('X Distance Along Model Space (km)')
    plt.ylabel('Elevation (km)')

    sxs, sys = zip(*sorted(zip(sxs, sys)))
    plt.plot(sxs, sys)
    plt.contourf(xs, ys, vs, levels=cfg.levels, cmap=cfg.colormap)

    add_colorbar(cfg)

    save(os.path.join(cfg.output_root, 'combined_temperature_position_{}.pdf'.format(count)))


def make_forward(cfg, xs, ys):
    log('making forward')
    plt.xlabel('X Distance Along Model Space (km)')
    plt.ylabel('Age (Ma)')
    plt.title('Sample Forward')

    plt.plot(xs, ys)
    save(os.path.join(cfg.output_root, 'sample_forward.pdf'))


def make_sample_positions(count, cfg, xs, ys):
    log('making sample positions')

    plt.xlabel('X Distance Along Model Space (km)')
    plt.ylabel('Elevation (km)')
    plt.title('Sample Position')

    xs, ys = zip(*sorted(zip(xs, ys)))
    plt.plot(xs, ys)
    save(os.path.join(cfg.output_root, 'sample_position_{}.pdf'.format(count)))


def make_topography(count, cfg, xs, ys):
    log('making topography')

    plt.xlabel('X Distance Along Model Space (km)')
    plt.ylabel('Elevation (km)')
    plt.title('Topography')
    plt.plot(xs, ys)
    save(os.path.join(cfg.output_root, 'topography_{}.pdf'.format(count)))


def make_isotherms(count, cfg, xs, ys, vs):
    log('making isotherms')

    plt.xlabel('X Distance Along Model Space (km)')
    plt.ylabel('Elevation (km)')
    plt.title('Isotherms (C)')
    plt.contour(xs, ys, vs, levels=cfg.isotherms, colors='red')
    save(os.path.join(cfg.output_root, 'isotherms_{}.pdf'.format(count)))


def make_temperature_plot(count, cfg, xs, ys, vs):
    log('making temperature')
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


def save(opath):
    plt.tight_layout()
    pp = PdfPages(opath)
    pp.savefig()
    pp.close()
    plt.clf()
# ============= EOF =============================================
