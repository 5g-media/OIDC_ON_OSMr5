#### HOWTO add OpenID Connect support to OSM r5 using Keycloak IdP #### 

The instructions below are parametric:
<GITHUB_BASE_URL> is the base URL of the project on Github
<BASE_PATH> is the base path of the cloned sources

1) download and unzip Keycloak v4.5.0 (https://www.keycloak.org/archive/downloads-4.5.0.html)
wget  https://downloads.jboss.org/keycloak/4.5.0.Final/adapters/keycloak-oidc/keycloak-wildfly-adapter-dist-4.5.0.Final.zip
unzip https://downloads.jboss.org/keycloak/4.5.0.Final/adapters/keycloak-oidc/keycloak-wildfly-adapter-dist-4.5.0.Final.zip
cd keycloak-wildfly-adapter-dist-4.5.0.Final 
./bin/standalone.sh -b=0.0.0.0

2) configure Keycloak - the instructions below report an example with a local OSM instance on VirtualBox available at 10.20.0.108
start keycloak and create a default admin user
for each OSM instance, in the "Clients" menu:
- define a "client" (e.g. "osm1"), set the callback URL (e.g. http://10.20.0.108/callback), in "access type" configure "confidential", get the "Secret" form "Credentials" and put it into NBI nbi.cfg
- define a role in "roles", one for each different OSM users (e.g. admin)
- create a keycloak user and set the credentials (e.g. testosm1/testosm1); then, in "role mapping", add a "client" + "client role" mapping 

3) install OSM R5 tag "v5.0.5" (the latest R5 tag available on date 11.02.2019)

Note: the OSM tag matches to DOCKERHUB tag (https://hub.docker.com/r/opensourcemano/nbi/tags) and to GIT tag for each component (e.g. https://osm.etsi.org/gitweb/?p=osm%2FNBI.git;a=shortlog;h=refs%2Fheads%2Fv5.0)

OSM v5.0.5 installation can be replicated with ./install_osm.sh -R v5.0.5 (from binaries) or ./install_osm.sh -b v5.0.5 (from sources)
(see https://osm.etsi.org/wikipub/index.php/Advanced_OSM_installation_procedures) 

Note: if osmclient install fails, redo the installation with the instructions here "https://osm.etsi.org/wikipub/index.php/OSM_client#Installation" AND using the tag v5.0.5

4) apply patches to NBI and LW-UI
see https://osm.etsi.org/wikipub/index.php/How_to_upgrade_the_OSM_Platform#Upgrading_a_specific_component_to_use_your_own_cloned_repo_.28e.g._for_developing_purposes.29

from OSM VM
git clone <GITHUB_BASE_URL>/OIDC_on_OSMr5
cp OIDC_on_OSMr5/*.sh .

#stop OSM
docker stack rm osm && sleep 60

#download patches
rm -fr OIDC_on_OSMr5
git clone <GITHUB_BASE_URL>/OIDC_on_OSMr5

#apply patch on NBI
rm -fr NBI
git clone -b v5.0.5 https://osm.etsi.org/gerrit/osm/NBI 
cd NBI
patch -p1 -i ../OIDC_on_OSMr5/PATCH/NBI.patch
cd ..
#build a new NBI container and update OSM service
#change NBI/Dockerfile.local with python3 mock.py for test
docker image rm `docker images | grep nbi | grep develop | awk '{print $1 ":" $2}'`
docker build NBI -f NBI/Dockerfile.local -t opensourcemano/nbi:develop --no-cache

#apply patch on LW-UI
rm -fr LW-UI
git clone -b v5.0.5 https://osm.etsi.org/gerrit/osm/LW-UI 
cd LW-UI
patch -p1 -i ../OIDC_on_OSMr5/PATCH/LW-UI.patch
cd ..

#build a new LW-UI container and update OSM service
#change LW-UI/docker/Dockerfile with python mock.py for test
docker image rm `docker images | grep light-ui | grep develop | awk '{print $1 ":" $2}'`
docker build LW-UI -f LW-UI/docker/Dockerfile -t opensourcemano/light-ui:develop --no-cache

#configure OSM to use NBI and LW-UI develop containers after restart/reboot
sudo sed -i "s/nbi\:\${TAG\:-latest}/nbi\:\${TAG\:-develop}/" /etc/osm/docker/docker-compose.yaml
sudo sed -i "s/light-ui\:\${TAG\:-latest}/light-ui\:\${TAG\:-develop}/" /etc/osm/docker/docker-compose.yaml

#start OSM
docker stack deploy -c /etc/osm/docker/docker-compose.yaml osm

ALLINONE: build_containers.sh
ALLINONE_MOCK: build_mock.sh


5) login on OSM using the keycloak user credentials 
- via browser ("authorization code flow")
open http://10.20.0.108, click on "OpenID Connect Sign In", login with Keycloak user credentials, have access to OSM UI automatically

- via API ("resource owner password credential flow")

get the a token ("my_token") from Keycloak using user credentials (username/password)
  curl --user client_id:client_secret -X POST \
  http://OIDC_SERVER:8080/auth/realms/master/protocol/openid-connect/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'cache-control: no-cache' \
  -d 'grant_type=password&username=myusername&password=mypassword'

use the Keycloak token ("my_token") to access protected resources on OSM
  curl -X GET \
  https://OSM_SERVER:9999/osm/admin/v1/projects \
  -H 'Content-Type: application/yaml' \
  -H 'cache-control: no-cache' \
  -H "Authorization: Bearer my_token"
  
  
#### HOWTO REPLICATE THE DEVELOPMENT ENVIRONMENT #### 

1) install OSM on VirtualBox and configure a static ip such as 10.20.0.108 with NAT + "host-only" adapters

#add to /etc/network/interfaces and restart networking service
auto enp0s8
iface enp0s8 inet static
address 10.20.0.108
netmask 255.255.255.0
network 10.20.0.0
broadcast 10.20.0.255

2) on OSM, disable nbi and lw-ui services
docker service scale osm_light-ui=0
docker service scale osm_nbi=0

3) on localhost, clone NBI and LW-UI components and apply the patches - see above

4) on localhost, install additional components according to https://osm.etsi.org/wikipub/index.php/Developer_HowTo

on MacOSX
sudo pip3 install pip==9.0.3
sudo pip3 install ptvsd==3.0.0


4a) prepare NBI development

#create a virtualenv to run Python3.6
virtualenv --python=/Library/Frameworks/Python.framework/Versions/3.6/bin/python nbi
source nbi/bin/activate

### configure gerrit commit-msg hook
curl -Lo NBI/.git/hooks/commit-msg http://osm.etsi.org/gerrit/tools/hooks/commit-msg
chmod u+x NBI/.git/hooks/commit-msg
cp NBI/.gitignore-common NBI/.gitignore
sudo pip3 install -e NBI

### install common
git clone https://osm.etsi.org/gerrit/osm/common
sudo pip3 install -e common

### change references to OSM services in /etc/hosts
10.20.0.108 mongo ro kafka nbi ro-db

### modify NBI/osm_nbi/nbi.cfg
log.screen: True
tools.staticdir.dir: "<BASE_PATH>/NBI/osm_nbi/html_public"
path: "<BASE_PATH>/NBI/osm_nbi/storage"

### prepare storage/kafka folders in NBI/osm_nbi
mkdir storage
cd storage
mkdir kafka
cd ../..
sudo mkdir /var/log/osm

### install pyang
#from the parent folder where NBI is
sudo pip3 install pyang
git clone https://github.com/robshakir/pyangbind
sudo pip3 install -e pyangbind
#if an error is produced: xcode-select --install

### copy yang models
scp ubuntu@10.20.0.108:/home/ubuntu/NBI/osm_nbi/* NBI/osm_nbi
mkdir -p IM/models/yang
scp ubuntu@10.20.0.108:/home/ubuntu/IM/models/yang/* IM/models/yang

#configure VSCode to run NBI
VS Code
{
    "name": "NBI local",
    "type": "python",
    "request": "launch",
    "program": "nbi.py",
    "console": "integratedTerminal"
}

4b) prepare LW-UI development

#create a virtualenv to run Python2.7
virtualenv --python=/usr/bin/python2.7 lw-ui

source lw-ui/bin/activate
pip install -r requirements.txt

#copy db.sqlite3 and static/bower_components from the lw-ui docker image docker in the root of LW-UI

#configure VSCode to run LW-UI
debug con Django
{
    "name": "LW-UI - Django",
    "type": "python",
    "request": "launch",
    "program": "${workspaceFolder}/manage.py",
    "args": [
        "runserver",
        "0.0.0.0:8099",
        "--noreload",
        "--nothreading"
    ],
    "django": true
},


5) with OSM and Keycloak running, launch NBI + LW-UI from your IDE (e.g. VSCode) and debug 


NOTE: 
#to scale DOWN/UP containers in OSM
docker service scale osm_light-ui=0
docker service scale osm_nbi=0

#to check logs
docker service logs osm_light-ui
docker service logs osm_nbi



