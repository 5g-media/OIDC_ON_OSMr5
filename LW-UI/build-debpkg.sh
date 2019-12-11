#!/bin/bash
# Copyright 2018 Telefonica
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


PKG_DIRECTORIES="authosm descriptorhandler instancehandler lib projecthandler sdnctrlhandler sf_t3d static template userhandler vimhandler packagehandler netslicehandler"
PKG_FILES="bower.json django.ini LICENSE manage.py nginx-app.conf README.md requirements.txt supervisor-app.conf .bowerrc"
MDG_NAME=lightui
DEB_INSTALL=debian/osm-${MDG_NAME}.install
export DEBEMAIL="gerardo.garciadeblas@telefonica.com"
export DEBFULLNAME="Gerardo Garcia"

PKG_VERSION=$(git describe --match "v*" --tags --abbrev=0)
PKG_VERSION_PREFIX=$(echo $PKG_VERSION | sed -e 's/v//g')
PKG_VERSION_POST=$(git rev-list $PKG_VERSION..HEAD | wc -l)
if [ "$PKG_VERSION_POST" -eq 0 ]; then
    PKG_DIR="deb_dist/osm-${MDG_NAME}-${PKG_VERSION_PREFIX}"
else
    PKG_DIR="deb_dist/osm-${MDG_NAME}-$PKG_VERSION_PREFIX.post${PKG_VERSION_POST}"
fi

rm -rf $PKG_DIR
rm -f *.orig.tar.xz
rm -f *.deb
rm -f $DEB_INSTALL
mkdir -p $PKG_DIR

for dir in $PKG_DIRECTORIES; do
    ln -s $PWD/$dir $PKG_DIR/.
    echo "$dir/* usr/share/osm-$MDG_NAME/$dir" >> $DEB_INSTALL
done
for f in $PKG_FILES; do
    cp $f $PKG_DIR/.
    echo "$f usr/share/osm-$MDG_NAME" >> $DEB_INSTALL
done
cp -R debian $PKG_DIR/.

pushd $PKG_DIR
dh_make -y --indep --createorig --a -c apache
dpkg-buildpackage -uc -us -tc -rfakeroot
popd


