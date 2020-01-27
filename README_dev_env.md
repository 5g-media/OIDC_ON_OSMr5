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



