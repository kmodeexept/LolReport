#!/bin/bash
python3 -m venv venv
cd venv/lib/python3*/site-package/
zip -r package.zip *
cd ../../../../