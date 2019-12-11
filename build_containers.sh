
rm -fr NBI
git clone -b v5.0.5 https://osm.etsi.org/gerrit/osm/NBI 
cd NBI
patch -p1 -i ../PATCH/NBI.patch
cd ..
docker build NBI -f NBI/Dockerfile.local -t opensourcemano/nbi:oidc --no-cache

rm -fr LW-UI
git clone -b v5.0.5 https://osm.etsi.org/gerrit/osm/LW-UI 
cd LW-UI
patch -p1 -i ../PATCH/LW-UI.patch
cd ..
docker build LW-UI -f LW-UI/docker/Dockerfile -t opensourcemano/light-ui:oidc --no-cache

docker stack rm osm && sleep 60
docker stack deploy -c /etc/osm/docker/docker-compose.yaml osm
