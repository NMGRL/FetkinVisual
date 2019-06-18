#!/usr/bin/env bash

CONDA=$HOME/Miniconda3
CONDA_ENV=FetkinVisual
ROOT=$HOME/FetkinVisual

$CONDA/envs/$CONDA_ENV/python.exe $ROOT/vis.py "$@"