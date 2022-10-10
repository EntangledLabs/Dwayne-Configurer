#!/bin/bash

apt update
apt dist-upgrade -y
apt autoremove -y

apt install git -y
apt install gccgo-go -y

git clone https://github.com/DSU-DefSec/DWAYNE-INATOR-5000.git -q ../dwayne

python3 main.py

cp ./output/dwayne* ../dwayne/