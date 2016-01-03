#!/bin/bash

set -e

cd "${BASH_SOURCE[0]}"

mkdir -p /opt/venv
/opt/miniconda2/bin/conda create -p /opt/venv/foodnemo python
source /opt/venv/foodnemo/bin/activate

pip install -r requirements
cp nginx.conf /etc/nginx/sites-available/foodnemo.com
ln -s /etc/nginx/sites-{available,enabled}/foodnemo.com
nginx -s reload
