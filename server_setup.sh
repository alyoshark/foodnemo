sudo pkg install gmake git

curl -k https://openresty.org/download/ngx_openresty-1.9.3.2.tar.gz | tar xf -
cd ngx_openresty-1.9.3.2
./configure
gmake && sudo gmake install

sudo ln -s /usr/local/openresty/nginx/sbin/nginx /sbin/nginx
sudo ln -s /usr/local/openresty/bin/resty /bin/resty
sudo ln -s /usr/local/openresty/luajit/bin/luajit-2.1.0-beta1 /bin/luajit
