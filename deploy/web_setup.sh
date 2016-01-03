#!/bin/bash

set -e

cd "$( dirname "${BASH_SOURCE[0]}")"

export PATH=$PATH:/opt/miniconda2/bin

mkdir -p /opt/venv

if [ ! -f /opt/venv/foodnemo/bin/activate ]; then
    conda create -p /opt/venv/foodnemo python
fi
source activate /opt/venv/foodnemo

pip install -r requirements
cp nginx.conf /etc/nginx/sites-available/foodnemo.com
ln -s /etc/nginx/sites-{available,enabled}/foodnemo.com
nginx -s reload
