#!/bin/bash
swig -python getter.i

python setup.py build_ext --inplace
