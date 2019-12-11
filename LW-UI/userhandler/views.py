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

from django.shortcuts import render, redirect
from sf_t3d.decorators import login_required
from django.http import HttpResponse
import json
import logging
import authosm.utils as osmutils
from lib.osm.osmclient.clientv2 import Client

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


@login_required
def user_list(request):
    user = osmutils.get_user(request)
    client = Client()
    result = client.user_list(user.get_token())
    result = {
        'users': result['data'] if result and result['error'] is False else []
    }
    return __response_handler(request, result, 'user_list.html')


@login_required
def create(request):
    user = osmutils.get_user(request)
    client = Client()
    user_data ={
        "username": request.POST['username'],
        "password": request.POST['password'],
        "projects": request.POST.getlist('projects')
    }

    result = client.user_create(user.get_token(), user_data)

    return __response_handler(request, result, 'users:list', to_redirect=True)


@login_required
def delete(request, user_id=None):
    user = osmutils.get_user(request)
    try:
        client = Client()
        del_res = client.user_delete(user.get_token(), user_id)
    except Exception as e:
        log.exception(e)
    return __response_handler(request, {}, 'users:list', to_redirect=True, )

@login_required
def update(request, user_id=None):
    user = osmutils.get_user(request)
    try:
        client = Client()
        projects_old = request.POST.get('projects_old').split(',')
        projects_new = request.POST.getlist('projects')
        default_project = request.POST.get('default_project')
        projects_new.append(default_project)
        projects_to_add = list(set(projects_new) - set(projects_old))
        projects_to_remove = list(set(projects_old) - set(projects_new))

        project_payload = {}

        for p in projects_to_remove:
            project_payload["$"+str(p)] = None
        for p in projects_to_add:
            if p not in projects_old:
                project_payload["$+"+str(p)] = str(p)
        project_payload["$" + default_project] = None
        project_payload["$+[0]"] = default_project
        payload = {}
        if project_payload:
            payload["projects"] = project_payload
        if request.POST.get('password') and request.POST.get('password') is not '':
            payload["password"] = request.POST.get('password')

        update_res = client.user_update(user.get_token(), user_id, payload)
    except Exception as e:
        log.exception(e)
        update_res = {'error': True, 'data': str(e)}
    if update_res['error']:
        return __response_handler(request, update_res['data'], url=None,
                                  status=update_res['data']['status'] if 'status' in update_res['data'] else 500)
    else:
        return __response_handler(request, {}, url=None, status=200)
        #return __response_handler(request, {}, 'users:list', to_redirect=True, )


def __response_handler(request, data_res, url=None, to_redirect=None, *args, **kwargs):
    raw_content_types = request.META.get('HTTP_ACCEPT', '*/*').split(',')
    if 'application/json' in raw_content_types or url is None:
        return HttpResponse(json.dumps(data_res), content_type="application/json", *args, **kwargs)
    elif to_redirect:
        return redirect(url, *args, **kwargs)
    else:
        return render(request, url, data_res)
