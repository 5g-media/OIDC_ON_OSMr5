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

import yaml
import json
import logging
from sf_t3d.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from lib.util import Util
import authosm.utils as osmutils
from lib.osm.osmclient.clientv2 import Client

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('instancehandler/view.py')

@login_required
def list(request):
    user = osmutils.get_user(request)
    client = Client()
    result = {}
    result_client = client.nst_list(user.get_token())

    result['templates'] = result_client['data'] if result_client and result_client['error'] is False else []

    return __response_handler(request, result, 'nst_list.html')

@login_required
def create_template(request, template_id=None):
    return

@login_required
def edit(request, template_id=None):
    user = osmutils.get_user(request)
    client = Client()
    if request.method == 'GET':
        page = 'nst_edit.html'
        result = client.nst_content(user.get_token(), template_id)
        if result['error']:
            return __response_handler(request, result, url=page, status=500)
        else:
            return __response_handler(request, {'template': {'template_id': str(template_id),  'data': result['data']}}, url=page, status=200)
    elif request.method == 'POST':
        result = client.nst_content_update(user.get_token(), template_id, request.POST.get('text'))
        if result['error'] == True:
            return __response_handler(request, result['data'], url=None, status=result['data']['status'] if 'status' in result['data'] else 500)
        else:
            return __response_handler(request, {}, url=None, status=200)


@login_required
def details(request, template_id=None):
    user = osmutils.get_user(request)
    client = Client()
    result = client.nst_details(user.get_token(), template_id)
    if result['error']:
        return __response_handler(request, result['data'], url=None, status=result['data']['status'] if 'status' in result['data'] else 500)
    else:
        return __response_handler(request, result, url=None, status=200)

@login_required
def delete_template(request, template_id=None):
    user = osmutils.get_user(request)
    
    client = Client()
    result = client.nst_delete(user.get_token(), template_id)
    
    if result['error']:
        return __response_handler(request, result['data'], url=None, status=result['data']['status'] if 'status' in result['data'] else 500)
    else:
        return __response_handler(request, {}, url=None, status=200)


@login_required
def download_template(request, package_id=None):
    return

@login_required
def onboard_template(request):
    user = osmutils.get_user(request)
    if request.method == 'POST':
        data_type = request.POST.get('type')
        if data_type == "file":
            file_uploaded = request.FILES['file']
            try:
                client = Client()
                result = client.nst_onboard(user.get_token(), file_uploaded)
            except Exception as e:
                log.exception(e)
                result = {'error': True, 'data': str(e)}
        else:
            result = {'error': True, 'data': 'Create descriptor: Unknown data type'}

        if result['error']:
            return __response_handler(request, result['data'], url=None, status=result['data']['status'] if 'status' in result['data'] else 500)
        else:
            return __response_handler(request, {}, url=None, status=200)


def __response_handler(request, data_res, url=None, to_redirect=None, *args, **kwargs):
    raw_content_types = request.META.get('HTTP_ACCEPT', '*/*').split(',')
    if not to_redirect and ('application/json' in raw_content_types or url is None):
        return HttpResponse(json.dumps(data_res), content_type="application/json", *args, **kwargs)
    elif to_redirect:
        return redirect(url, *args, **kwargs)
    else:
        return render(request, url, data_res)