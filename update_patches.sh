rm -fr NBI
git clone -b v5.0.5 https://osm.etsi.org/gerrit/osm/NBI
rm -fr NBI/.gi*
diff -rc --new-file NBI/   NBI_MODIFIED/   > PATCH/NBI.patch

rm -fr LW-UI
git clone -b v5.0.5 https://osm.etsi.org/gerrit/osm/LW-UI
rm -fr LW-UI/.gi*
diff -rc --new-file LW-UI/ LW-UI_MODIFIED/ > PATCH/LW-UI.patch

