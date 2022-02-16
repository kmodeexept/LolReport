#!/bin/bash

zip -g package.zip lambda_function.py
zip -g package.zip template_website.html
zip -g package.zip api.key 
aws lambda update-function-code --function-name webSite --zip-file fileb://package.zip
