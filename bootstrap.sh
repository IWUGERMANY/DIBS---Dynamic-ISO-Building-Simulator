#!/bin/bash

# Generating locale, can be an issue on fresh DO servers
export LANGUAGE=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
sudo locale-gen en_US.UTF-8
sudo dpkg-reconfigure locales

# Update and upgrade without requiring manual GRUB configuration
# To make GRUB headless https://askubuntu.com/questions/146921/how-do-i-apt-get-y-dist-upgrade-without-a-grub-config-prompt
# To not mess up encoding https://stackoverflow.com/questions/18471764/vagrant-provisioning-switches-character-encoding
unset UCF_FORCE_CONFFOLD
export UCF_FORCE_CONFFNEW=YES
ucf --purge /boot/grub/menu.lst

export DEBIAN_FRONTEND=noninteractive
apt-get update
# sudo apt-get -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confnew" -o Dpkg::Options::="--force-confold" --force-yes -fuy dist-upgrade

# Create swap space for installation of lxml https://stackoverflow.com/a/26762938
sudo dd if=/dev/zero of=/swapfile bs=1024 count=524288
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Installation of foodcampus-specific packages
sudo apt-get install -y libpq-dev python3-dev libjpeg-dev libjpeg8 zlib1g libfreetype6

# Insall everything
echo Downloading Pip...
wget https://bootstrap.pypa.io/get-pip.py >/dev/null 2>&1
python3 get-pip.py
pip3 install virtualenvwrapper
echo $PWD
pip3 install -r /vagrant/requirements.txt


# Pandas Fails to install with Pip3!!! Installation being annoying
echo Installing Pandas with sudo apt get
sudo apt-get install python3-pandas -y


# Echo virtualenvironment things into bashrc, also for python3 compatibility
echo "
VIRTUALENVWRAPPER_PYTHON='/usr/bin/python3'
export WORKON_HOME=/rc-simulator/.virtualenvs
export PROJECT_HOME=/rc-simulator/
source /usr/local/bin/virtualenvwrapper.sh
cd /rc-simulator/
workon rc_simulator
" >> /home/vagrant/.bashrc

# Unmount swap
sudo swapoff -a
sudo locale-gen en_US.UTF-8
