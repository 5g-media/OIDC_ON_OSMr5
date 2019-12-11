sudo sed -i "s/nbi\:\${TAG\:-latest}/nbi\:\${TAG\:-oidc}/" /etc/osm/docker/docker-compose.yaml
sudo sed -i "s/light-ui\:\${TAG\:-latest}/light-ui\:\${TAG\:-oidc}/" /etc/osm/docker/docker-compose.yaml
