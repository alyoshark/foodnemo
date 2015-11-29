cd $HOME
sudo pip install virtualenv
mkdir -p venv
python2 -mvirtualenv venv/foodnemo
source $HOME/venv/foodnemo/bin/activate.csh

if ( -d foodnemo ) then
    git clone https://github.com/xch91/foodnemo.git
fi

cd foodnemo
git pull

pip install -r deploy/requirements

mkdir -p raw static
