sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && locale-gen
export HOME=/root
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8
export LC_ALL=en_US.UTF-8
. /sandbox/env.sh

cp /sandbox/code/github/threefoldtech/digitalmeX/packages/bootstrap_bot/chatflows/bootstrap_bot.py /sandbox/code/github/threefoldtech/digitalmeX/DigitalMe/tools/openpublish/base_chatflows/

rm -r /sandbox/cfg/nacl/*

kosmos --instruct /bot_configure.toml
