#
#   Copyright 2018 EveryUP Srl
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an  BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
from django.core.exceptions import PermissionDenied

from .models import OsmUser
from lib.osm.osmclient.clientv2 import Client
from .exceptions import OSMAuthException


class OsmBackend(object):

    def authenticate(self, **kwargs):
        '''
        kwargs will receive the python dict that may contain
        {username, password, project-id}  to authenticate
        '''
        if all(k in kwargs for k in ('username', 'password', 'project_id')):
            username = kwargs['username']
            password = kwargs['password']

            client = Client()
            result = client.auth(kwargs)

            if 'error' in result and result['error'] is True:
                raise OSMAuthException(result['data'])
            else:

                try:
                    user = OsmUser.objects.get(username=username)
                    user.psw = password
                    user.token = result['data']['id']
                    user.project_id = result['data']['project_id']
                    user.token_expires = result['data']['expires']
                    user.is_admin = bool(result['data']['admin'])
                    user.save()
                except OsmUser.DoesNotExist:
                    user = OsmUser(username=username, psw=password, token=result['data']['id'],
                                   project_id=result['data']['project_id'],
                                   token_expires=result['data']['expires'], is_admin=result['data']['admin'])
                    user.save()

                return user

        return None

    def get_user(self, user_id):
        try:
            return OsmUser.objects.get(pk=user_id)
        except OsmUser.DoesNotExist:
            return None
