#!/bin/bash

echo
echo "+================================"
echo "| START: lunch"
echo "+================================"
echo

source backend/.env

datehash=`date | md5sum | cut -d" " -f1`
abbrvhash=${datehash: -8}

echo 
echo "Building container using tag ${abbrvhash}"
echo
docker build -t graboskyc/lunch:latest -t graboskyc/lunch:${abbrvhash} .

EXITCODE=$?

if [ $EXITCODE -eq 0 ]
    then

    echo 
    echo "Starting container"
    echo
    docker stop lunch
    docker rm lunch
    docker run -t -i -d -p 8000:8000 --name lunch -e "LUNCHURL=${LUNCHURL}" --restart unless-stopped graboskyc/lunch:${abbrvhash}

    echo
    echo "+================================"
    echo "| END:  lunch"
    echo "+================================"
    echo
else
    echo
    echo "+================================"
    echo "| ERROR: Build failed"
    echo "+================================"
    echo
fi