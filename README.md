### OpenID Connect support in OSM r5 using Keycloak IDP ### 

The instructions allow to replicate the tests on a local VM with fixed IP, e.g. on a VirtualBox 

1) on VirtualBox, create a VM with 8GB RAM, 30GB DISK, add a secondary network adapter (so, NAT + "host-only" adapters) 
2) configure a static ip such as 10.20.0.155 on the "host-only" adapter

- add to /etc/network/interfaces and restart networking service

```
auto enp0s8
iface enp0s8 inet static
address 10.20.0.155
netmask 255.255.255.0
network 10.20.0.0
broadcast 10.20.0.255
```

3) from a clean Ubuntu16.04 server image, install pre-requirements, download and unzip Keycloak v4.5.0, change KeyCloak port 8443 to 8143

```
sudo apt-get install -y unzip
sudo apt-get install -y openjdk-8-jdk

wget  https://downloads.jboss.org/keycloak/4.5.0.Final/keycloak-4.5.0.Final.zip
unzip keycloak-4.5.0.Final.zip
cd keycloak-4.5.0.Final
#change 8443 port in standalone/configuration/standalone.xml, e.g. from 8443 to 8143
nohup ./bin/standalone.sh -b=0.0.0.0 &
```

4) configure Keycloak (the example below are for a local OSM instance at 10.20.0.155)
* start keycloak and create a default admin user
* create the realm "osm"
* for each OSM instance, in the "Clients" menu:
    * define a "client" (e.g. "osm1"), set the callback URL (e.g. http://10.20.0.155/callback), in "access type" configure "confidential", get the "Secret" from "Credentials" and use it later into the NBI nbi.cfg
    * define a role in "client -> roles", one for each different OSM user type (e.g. admin)
    * create a keycloak user and set the credentials (e.g. testosm1/testosm1); then, in "role mapping", add a "client" + "client role" mapping, so that testosm1 will impersonate, for each client (e.g. osm1, osm2, etc.), the specific client-role (e.g. admin)

5) install OSM R5 tag "v5.0.5"

Note: the OSM tag matches to [DOCKERHUB tag](https://hub.docker.com/r/opensourcemano/nbi/tags) and to GIT tag for [each component](e.g. https://osm.etsi.org/gitweb/?p=osm%2FNBI.git;a=shortlog;h=refs%2Fheads%2Fv5.0)

OSM v5.0.5 installation can be replicated with `./install_osm.sh -t v5.0.5`
see [OSM instructions](https://osm.etsi.org/wikipub/index.php/Advanced_OSM_installation_procedures) 
and [specific v5.0.5 instructions](https://osm.etsi.org/wikipub/index.php/OSM_Release_FIVE) 

6) fix docker-compose for v5.0.5 [pointing to v5.0.5](https://osm.etsi.org/wikipub/index.php/How_to_upgrade_the_OSM_Platform), then start OSM

```

sudo sed -i "s/ro\:\${TAG\:-latest}/ro\:v5.0.5/" /etc/osm/docker/docker-compose.yaml
sudo sed -i "s/lcm\:\${TAG\:-latest}/lcm\:v5.0.5/" /etc/osm/docker/docker-compose.yaml
sudo sed -i "s/mon\:\${TAG\:-latest}/mon\:v5.0.5/" /etc/osm/docker/docker-compose.yaml
sudo sed -i "s/pol\:\${TAG\:-latest}/pol\:v5.0.5/" /etc/osm/docker/docker-compose.yaml
sudo sed -i "s/nbi\:\${TAG\:-latest}/nbi\:v5.0.5/" /etc/osm/docker/docker-compose.yaml
sudo sed -i "s/light-ui\:\${TAG\:-latest}/light-ui\:v5.0.5/" /etc/osm/docker/docker-compose.yaml
sudo sed -i "s/keystone\:\${TAG\:-latest}/keystone\:v5.0.5/" /etc/osm/docker/docker-compose.yaml

docker stack remove osm && sleep 60
docker stack deploy -c /etc/osm/docker/docker-compose.yaml osm
```

OPTIONAL: fix MTU with fix_mtu.sh script

7) apply [patches to NBI and LW-UI](https://osm.etsi.org/wikipub/index.php/How_to_upgrade_the_OSM_Platform#Upgrading_a_specific_component_to_use_your_own_cloned_repo_.28e.g._for_developing_purposes.29)

- clone scripts from OSM VM

```
git clone https://github.com/5g-media/OIDC_ON_OSMr5.git
cp OIDC_ON_OSMr5/*.sh .
```

- stop OSM

```
docker stack rm osm && sleep 60
```


- apply patch on NBI, change the /app/NBI/osm_nbi/nbi.cfg and build the container image

```
rm -fr NBI
git clone -b v5.0.5 https://osm.etsi.org/gerrit/osm/NBI 
cd NBI
patch -p1 -i ../OIDC_ON_OSMr5/PATCH/NBI.patch
cd ..

#OPTIONAL docker images rm `docker images | grep nbi | grep v5.0.5 | awk '{print $1 ":" $2}'`
#change /app/NBI/osm_nbi/nbi.cfg with the KeyCloak configuration: at least "secret" will be different, see KeyCloak configuration above
docker build NBI -f NBI/Dockerfile.local -t opensourcemano/nbi:v5.0.5OIDC --no-cache
```
  

- apply patch on LW-UI, change the /usr/share/osm-lightui/sf_t3d/settings.py and build the container image

```
rm -fr LW-UI
git clone -b v5.0.5 https://osm.etsi.org/gerrit/osm/LW-UI 
cd LW-UI
patch -p1 -i ../OIDC_ON_OSMr5/PATCH/LW-UI.patch
cd ..

#OPTIONAL docker images rm `docker images | grep light-ui | grep v5.0.5 | awk '{print $1 ":" $2}'`
#change /usr/share/osm-lightui/sf_t3d/settings.py with the KeyCloak configuration
docker build LW-UI -f LW-UI/docker/Dockerfile -t opensourcemano/light-ui:v5.0.5OIDC --no-cache
```

- configure OSM to use NBI and LW-UI develop containers after restart/reboot

```
sudo sed -i "s/nbi\:v5.0.5/nbi\:v5.0.5OIDC/" /etc/osm/docker/docker-compose.yaml
sudo sed -i "s/light-ui\:v5.0.5/light-ui\:v5.0.5OIDC/" /etc/osm/docker/docker-compose.yaml
```
- deploy OSM

```
docker stack deploy -c /etc/osm/docker/docker-compose.yaml osm
```


8) OPTIONAL - if needed, configure OIDC on NBI and LW-UI **AFTER** the containers are built

NBI

```
docker cp `docker ps | grep nbi | awk '{print $1}'`:/app/NBI/osm_nbi/nbi.cfg nbi.cfg
```
change nbi.cfg and update OSM..

```
docker config create nbi.cfg nbi.cfg
docker service update --config-add source=nbi.cfg,target=/app/NBI/osm_nbi/nbi.cfg,mode=0440 osm_nbi
```

..or update the existing configuration

```
docker service update --config-rm nbi.cfg --config-add source=nbi.cfg,target=/app/NBI/osm_nbi/nbi.cfg,mode=0440 osm_nbi
```

LW-UI

```
docker cp  `docker ps | grep light | awk '{print $1}'`:/usr/share/osm-lightui/sf_t3d/settings.py settings.py
```
change settings.py and update OSM..

```
docker config create settings.py settings.py
docker service update --config-add source=settings.py,target=/usr/share/osm-lightui/sf_t3d/settings.py,mode=0440 osm_light-ui
```

..or update the existing configuration

```
docker service update --config-rm settings.py --config-add source=settings.py,target=/usr/share/osm-lightui/sf_t3d/settings.py,mode=0440 osm_light-ui
```

9) login on OSM using the keycloak user credentials 

**UI (browser)** ("authorization code flow")
open http://10.20.0.155, click on "OpenID Connect Sign In", login with Keycloak user credentials (testosm1/testosm1), get access to OSM UI automatically

**M2M (API)** ("resource owner password credential flow")
1) get the a token from Keycloak using user credentials (username/password)

```
ACCESS_TOKEN=$(curl --location --request POST 'http://10.20.0.155:8080/auth/realms/osm/protocol/openid-connect/token' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'grant_type=password' \
--data-urlencode 'client_id=osm1' \
--data-urlencode 'client_secret=beb35e44-4084-48e9-967e-da7ec584b3c9' \
--data-urlencode 'username=testosm1' \
--data-urlencode 'password=testosm1' | jq -r '.access_token')
```

OPTIONAL: in case of SSL errors, please check the KeyCloak "SSL required" option for the osm realm 

2) use token to access protected resources on OSM

```
  curl -k -X GET \
  https://10.20.0.155:9999/osm/admin/v1/projects \
  -H 'Content-Type: application/yaml' \
  -H 'cache-control: no-cache' \
  -H "Authorization: Bearer $ACCESS_TOKEN"
 ```
  
  

#### HOWTO REPLICATE THE DEVELOPMENT ENVIRONMENT #### 

1) on OSM, disable nbi and lw-ui services

```
docker service scale osm_light-ui=0
docker service scale osm_nbi=0
```

2) on localhost, clone NBI and LW-UI components and apply the patches - see above

3) on localhost, install additional components according to https://osm.etsi.org/wikipub/index.php/Developer_HowTo

on MacOSX

```
sudo pip3 install pip==9.0.3
sudo pip3 install ptvsd==3.0.0
```

4) prepare NBI development

- create a virtualenv to run Python3.6

```
virtualenv --python=/Library/Frameworks/Python.framework/Versions/3.6/bin/python nbi
source nbi/bin/activate
```

- configure gerrit commit-msg hook

```
curl -Lo NBI/.git/hooks/commit-msg http://osm.etsi.org/gerrit/tools/hooks/commit-msg
chmod u+x NBI/.git/hooks/commit-msg
cp NBI/.gitignore-common NBI/.gitignore
sudo pip3 install -e NBI
```

- install common

```
git clone https://osm.etsi.org/gerrit/osm/common
sudo pip3 install -e common
```

- change references to OSM services in /etc/hosts

```
10.20.0.155 mongo ro kafka nbi ro-db
```

- modify NBI/osm_nbi/nbi.cfg

```
log.screen: True
tools.staticdir.dir: "<BASE_PATH>/NBI/osm_nbi/html_public"
path: "<BASE_PATH>/NBI/osm_nbi/storage"
```

- prepare storage/kafka folders in NBI/osm_nbi

```
mkdir storage
cd storage
mkdir kafka
cd ../..
sudo mkdir /var/log/osm
```

- install pyang; from the parent folder where NBI is

```
sudo pip3 install pyang
git clone https://github.com/robshakir/pyangbind
sudo pip3 install -e pyangbind
```

- if an error is produced: `xcode-select --install`

- copy yang models

```
scp ubuntu@10.20.0.155:/home/ubuntu/NBI/osm_nbi/* NBI/osm_nbi
mkdir -p IM/models/yang
scp ubuntu@10.20.0.155:/home/ubuntu/IM/models/yang/* IM/models/yang
```

- configure VSCode to run NBI

```
VS Code
{
    "name": "NBI local",
    "type": "python",
    "request": "launch",
    "program": "nbi.py",
    "console": "integratedTerminal"
}
```

5) prepare LW-UI development

- create a virtualenv to run Python2.7

```
virtualenv --python=/usr/bin/python2.7 lw-ui

source lw-ui/bin/activate
pip install -r requirements.txt
```

- copy db.sqlite3 and static/bower_components from the lw-ui docker image docker in the root of LW-UI

- configure VSCode to run LW-UI

```
debug with Django
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
```

6) with OSM and Keycloak running, launch NBI + LW-UI from your IDE (e.g. VSCode) and debug 


NOTE: to scale DOWN/UP containers in OSM

```
docker service scale osm_light-ui=0
docker service scale osm_nbi=0
```

- to check logs

```
docker service logs osm_light-ui
docker service logs osm_nbi
```

### Acknowledgements
This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 761699. The dissemination of results herein reflects only the author’s view and the European Commission is not responsible for any use that may be made of the information it contains.

