#!/usr/bin/env bash

CONDA=$HOME/miniconda3
CONDA_ENV=FetkinVisual
ROOT=$HOME/FetkinVisual

$CONDA/envs/$CONDA_ENV/bin/python $ROOT/vis.py "$@"