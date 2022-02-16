#!/bin/bash
python3 -m venv venv
source venv/bin/activate
pip install -r Requirements.txt
pythonver=$(ls venv/lib)
cd venv/lib/$pythonver/site-packages && zip -r ../../../../package.zip *