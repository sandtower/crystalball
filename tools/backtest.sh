#!/bin/sh
cd /home/crystalball/src
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
python -m app.backtest &
cd -
