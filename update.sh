#!/bin/bash

FILE=package.zip

if test -f "$FILE"; then
    echo "$FILE exists."
else
    echo "create venv and package"
    ./configure.sh
    echo "configure finished"
fi

zip -g $FILE lambda_function.py
zip -g $FILE template_website.html
zip -g $FILE api.key 
aws lambda update-function-code --function-name webSite --zip-file fileb://$FILE > /dev/null
