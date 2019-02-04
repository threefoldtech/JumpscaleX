#!/bin/bash
set -ex

# make output directory
ARCHIVE=/tmp/archives
FLIST=/tmp/flist
mkdir -p $ARCHIVE

# install system deps
apt-get update
apt-get install -y curl locales git wget netcat tar sudo tmux ssh python3-pip redis-server libffi-dev python3-dev libssl-dev libpython3-dev libssh-dev libsnappy-dev build-essential pkg-config libvirt-dev libsqlite3-dev -y


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

# cloning source code
curl https://raw.githubusercontent.com/threefoldtech/jumpscaleX/master/install/install.py?$RANDOM > /tmp/install.py;python3 /tmp/install.py 1 y
#ssh generate
ssh-keygen -f ~/.ssh/id_rsa -P ''
eval `ssh-agent -s`
ssh-add ~/.ssh/id_rsa
tar -cpzf "/tmp/archives/JSX.tar.gz" --exclude tmp --exclude dev --exclude sys --exclude proc  /