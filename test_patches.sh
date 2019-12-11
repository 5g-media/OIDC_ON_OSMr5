rm -fr TEST
mkdir TEST
cd TEST

echo TEST NBI PATCH
git clone -b v5.0.5 https://osm.etsi.org/gerrit/osm/NBI
rm -fr NBI/.gi*
mv NBI NBI_TO_BE_PATCHED
cd NBI_TO_BE_PATCHED

patch -p1 -i ../../PATCH/NBI.patch 
cd ..
diff -rc --new-file NBI_TO_BE_PATCHED/   ../NBI_MODIFIED/   > DIFF_NBI.patch
echo This shoud be empty
cat DIFF_NBI.patch
rm DIFF_NBI.patch

echo TEST LW-UI PATCH
git clone -b v5.0.5 https://osm.etsi.org/gerrit/osm/LW-UI
rm -fr LW-UI/.gi*
mv LW-UI LW-UI_TO_BE_PATCHED
cd LW-UI_TO_BE_PATCHED

patch -p1 -i ../../PATCH/LW-UI.patch 
cd ..
diff -rc --new-file LW-UI_TO_BE_PATCHED/   ../LW-UI_MODIFIED/   > DIFF_LW-UI.patch
echo This shoud be empty
cat DIFF_LW-UI.patch
rm DIFF_LW-UI.patch

cd ..
rm -fr TEST

