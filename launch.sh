#!/usr/bin/env bash
DIRNAME=$(dirname $(readlink -f $0))
cd ${DIRNAME}
${DIRNAME}/venv/bin/python ${DIRNAME}/main.py
cd /
