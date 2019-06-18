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
from numpy import array


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
# ============= EOF =============================================
