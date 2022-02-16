#!/bin/bash

zip -g package.zip lambda_function.py
aws lambda update-function-code --function-name webSite --zip-file fileb://function.zip
