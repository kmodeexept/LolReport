#!/bin/bash
python3 -m venv venv
pythonver=$(ls venv/lib)
cd venv/lib/$pythonver/site-packages && zip -r ../../../../package.zip *