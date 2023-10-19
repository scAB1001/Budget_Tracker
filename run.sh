#!/bin/bash
cd C:/Users/AB/OneDrive/Documents/CODE/C/WAD/
flask\Scripts\activate
export FLASK_APP=run.py
export FLASK_DEBUG=1
cd ./S2/
python ./run.py