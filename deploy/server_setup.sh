apt update
apt install -y nginx monit gcc libffi-dev libssl-dev

cd /opt
wget https://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh
bash miniconda.sh -b -p /opt/miniconda2

MONITRC=/etc/monit/monitrc
sed -i 's/set daemon 120/set daemon 10/g' $MONITRC
httpd_opened=`grep '^set httpd' $MONITRC | wc -l`
if [ $httpd_opened -eq 0 ]; then
    echo "set httpd port 2812 and
        use address localhost
        allow localhost
    " >> $MONITRC
fi
