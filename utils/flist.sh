#!/bin/bash
set -ex

# make output directory
ARCHIVE=/tmp/archives
FLIST=/tmp/flist
mkdir -p $ARCHIVE

# install system deps
apt-get update
apt-get install -y curl unzip rsync locales git lsb wget netcat tar sudo tmux ssh python3-pip redis-server libffi-dev python3-dev libssl-dev libpython3-dev libssh-dev libsnappy-dev build-essential pkg-config libvirt-dev libsqlite3-dev
pip3 install click

# setting up locales
if ! grep -q ^en_US /etc/locale.gen; then
    echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
    locale-gen en_US.UTF-8
    echo "export LC_ALL=en_US.UTF-8" >> /root/.bashrc
    echo "export LANG=en_US.UTF-8" >> /root/.bashrc
    echo "export LANGUAGE=en_US.UTF-8" >> /root/.bashrc
    echo " export HOME=/sandbox" >> /root/.bashrc
    export LC_ALL=en_US.UTF-8
    export LANG=en_US.UTF-8
    export LANGUAGE=en_US.UTF-8
fi

for target in /usr/local $HOME/opt $HOME/.ssh $HOME/opt/cfg $HOME/opt/bin $HOME/code $HOME/code/github $HOME/code/github/threefoldtech $HOME/code/github/threefoldtech/jumpscale_weblibs $HOME/opt/var/capnp $HOME/opt/var/log $HOME/jumpscale/cfg; do
    mkdir -p $target
    sudo chown -R $USER:$USER $target
done

pushd $HOME/code/github/threefoldtech

#ssh generate
eval `ssh-agent -s`
mkdir -p /root/.ssh
ssh-keygen -t rsa -N "" -f /root/.ssh/id_rsa -q -P ""; ssh-add /root/.ssh/id_rsa

# Install jumpscale
curl https://raw.githubusercontent.com/threefoldtech/jumpscaleX/development_jumpscale/install/jsx.py?$RANDOM > /tmp/jsx;
# change permission
chmod +x /tmp/jsx; 
/tmp/jsx configure -s --secret mysecret;
# install
/tmp/jsx install -s

#change in permission
chown root:root /tmp
. /sandbox/env.sh
cd /sandbox
kosmos "j.builders.runtimes.lua.install(reset=True)"
kosmos "j.builders.runtimes.lua.lua_rocks_install() "

cd /sandbox/code/github/threefoldtech/jumpscaleX/
tar -cpzf "/tmp/archives/JSX.tar.gz" --exclude dev --exclude sys --exclude proc  /
