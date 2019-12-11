#
#   Copyright 2018 CNIT - Consorzio Nazionale Interuniversitario per le Telecomunicazioni
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

from django.shortcuts import render, redirect
from sf_t3d.decorators import login_required
from django.http import HttpResponse
import json
import logging
import authosm.utils as osmutils
from lib.osm.osmclient.clientv2 import Client

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('sdnctrlhandler/view.py')


@login_required
def list(request):
    user = osmutils.get_user(request)
    project_id = user.project_id
    result = {'project_id': project_id}
    raw_content_types = request.META.get('HTTP_ACCEPT', '*/*').split(',')
    if 'application/json' not in raw_content_types:
        return __response_handler(request, result, 'sdn_list.html')
    client = Client()
    result_client = client.sdn_list(user.get_token())

    result['sdns'] = result_client['data'] if result_client and result_client['error'] is False else []

    return __response_handler(request, result, 'sdn_list.html')


@login_required
def create(request):
    user = osmutils.get_user(request)
    project_id = user.project_id
    result = {'project_id': project_id}
    if request.method == 'GET':
        return __response_handler(request, result, 'sdn_create.html')
    else:
        new_sdn_dict = request.POST.dict()
        client = Client()
        keys = ["name",
                "type",
                "version",
                "dpid",
                "ip",
                "port",
                "user",
                "password"]
        sdn_data = dict(filter(lambda i: i[0] in keys and len(i[1]) > 0, new_sdn_dict.items()))
        sdn_data['port'] = int(sdn_data['port'])

        result = client.sdn_create(user.get_token(), sdn_data)

        return __response_handler(request, result, 'sdns:list', to_redirect=True, )


@login_required
def delete(request, sdn_id=None):
    user = osmutils.get_user(request)
    project_id = user.project_id
    try:
        client = Client()
        del_res = client.sdn_delete(user.get_token(), sdn_id)
    except Exception as e:
        log.exception(e)
    return __response_handler(request, del_res, 'sdns:list', to_redirect=True, )


@login_required
def show(request, sdn_id=None):
    user = osmutils.get_user(request)
    project_id = user.project_id
    client = Client()
    result = client.sdn_get(user.get_token(), sdn_id)
    if isinstance(result, dict) and 'error' in result and result['error']:
        return render(request, 'error.html')
    return __response_handler(request, {
        "sdn": result['data'],
        "project_id": project_id})


def __response_handler(request, data_res, url=None, to_redirect=None, *args, **kwargs):
    raw_content_types = request.META.get('HTTP_ACCEPT', '*/*').split(',')
    if 'application/json' in raw_content_types or url is None:
        return HttpResponse(json.dumps(data_res), content_type="application/json", *args, **kwargs)
    elif to_redirect:
        return redirect(url, *args, **kwargs)
    else:
        return render(request, url, data_res)
