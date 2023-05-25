#!/bin/sh

rm -f ./*.tar.gz
ansible-galaxy collection build -v
TARBALL=$(ls -1 ./*.tar.gz)
ansible-galaxy collection publish -v "$TARBALL"
rm -f ./*.tar.gz
