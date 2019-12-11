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

import json
import logging

import yaml
from sf_t3d.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect


from lib.util import Util
from lib.osm.osmclient.clientv2 import Client
from lib.osm.osm_rdcl_parser import OsmParser
from lib.osm.osm_util import OsmUtil
import authosm.utils as osmutils

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('packagehandler/view.py')


@login_required
def show_packages(request, package_type=None):
    user = osmutils.get_user(request)
    project_id = user.project_id
    client = Client()
    filter = request.GET.get('type')
    try:
        if package_type == 'ns':
            descriptors = client.nsd_list(user.get_token(),filter)
        elif package_type == 'vnf':
            descriptors = client.vnfd_list(user.get_token(),filter)
    except Exception as e:
        log.exception(e)
        descriptors = []

    url = 'package_list.html'
    return __response_handler(request, {
        'descriptors': descriptors['data'] if descriptors and descriptors['error'] is False else [],
        'project_id': project_id,
        'project_type': 'osm',
        'package_type': package_type
    }, url)

@login_required
def create_package_empty(request, package_type=None):
    user = osmutils.get_user(request)
    pkg_name = request.POST.get('name', '')
    try:
        client = Client()
        if package_type == 'ns':
            result = client.nsd_create_pkg_base(user.get_token(), pkg_name)
        elif package_type == 'vnf':
            result = client.vnfd_create_pkg_base(user.get_token(), pkg_name)
        else:
            log.debug('Update descriptor: Unknown data type')
            result = {'error': True, 'data': 'Update descriptor: Unknown data type'}
    except Exception as e:
        log.exception(e)
        result = {'error': True, 'data': str(e)}

    if result['error'] == True:
        return __response_handler(request, result['data'], url=None,
                                  status=result['data']['status'] if 'status' in result['data'] else 500)
    else:
        result['data']['type'] = package_type
        return __response_handler(request, result, url=None, status=200)


@login_required
def delete_package(request, package_type=None, package_id=None):
    user = osmutils.get_user(request)
    project_id = user.project_id
    try:
        client = Client()
        if package_type == 'ns':
            result = client.nsd_delete(user.get_token(), package_id)
        elif package_type == 'vnf':
            result = client.vnfd_delete(user.get_token(), package_id)
    except Exception as e:
        log.exception(e)
        result = {'error': True, 'data': str(e)}

    url = 'package_list.html'
    descriptors = {}
    try:
        if package_type == 'ns':
            descriptors = client.nsd_list(user.get_token())
        elif package_type == 'vnf':
            descriptors = client.vnfd_list(user.get_token())
    except Exception as e:
        log.exception(e)

    return __response_handler(request, {
        'descriptors': descriptors['data'] if descriptors and descriptors['error'] is False else [],
        'project_id': project_id,
        'project_type': 'osm',
        'package_type': package_type,
        'alert_message': {
            'success': False if result['error'] is True else True,
            'message': 'An error occurred while processing your request.' if result and result['error'] is True else "Record deleted successfully"}
    }, url)

@login_required
def clone_package(request, package_type=None, package_id=None):
    user = osmutils.get_user(request)
    try:
        client = Client()
        if package_type == 'ns':
            result = client.nsd_clone(user.get_token(), package_id)
        elif package_type == 'vnf':
            result = client.vnfd_clone(user.get_token(), package_id)
        else:
            log.debug('Update descriptor: Unknown data type')
            result = {'error': True, 'data': 'Update descriptor: Unknown data type'}
    except Exception as e:
        log.exception(e)
        result = {'error': True, 'data': str(e)}
    if result['error'] == True:
        return __response_handler(request, result['data'], url=None,
                                  status=result['data']['status'] if 'status' in result['data'] else 500)
    else:
        return __response_handler(request, {}, url=None, status=200)

@login_required
def download_pkg(request, package_id, package_type):
    user = osmutils.get_user(request)
    file_name = "osm_export.tar.gz"
    tar_pkg = None
    try:
        client = Client()
        if package_type == 'ns':
            tar_pkg = client.get_nsd_pkg(user.get_token(), package_id)
        elif package_type == 'vnf':
            tar_pkg = client.get_vnfd_pkg(user.get_token(), package_id)

    except Exception as e:
        log.exception(e)
    
    response = HttpResponse(content_type="application/tgz")
    response["Content-Disposition"] = "attachment; filename="+ file_name
    response.write(tar_pkg.getvalue())
    return response

@login_required
def onboard_package(request, package_type=None):
    user = osmutils.get_user(request)
    if request.method == 'POST':
        data_type = request.POST.get('type')
        if data_type == "file":
            file_uploaded = request.FILES['file']

            try:
                client = Client()
                if package_type == 'ns':
                    result = client.nsd_onboard(user.get_token(), file_uploaded)
                elif package_type == 'vnf':
                    result = client.vnfd_onboard(user.get_token(), file_uploaded)
                else:
                    log.debug('Create descriptor: Unknown data type')
                    result = {'error': True, 'data': 'Create descriptor: Unknown data type'}

            except Exception as e:
                log.exception(e)
                result = {'error': True, 'data': str(e)}
        else:
            result = {'error': True, 'data': 'Create descriptor: Unknown data type'}

        if result['error']:
            return __response_handler(request, result['data'], url=None, status=result['data']['status'] if 'status' in result['data'] else 500)
        else:
            return __response_handler(request, {}, url=None, status=200)

@login_required
def get_package_files_list(request, package_id, package_type):
    user = osmutils.get_user(request)
    try:
        client = Client()
        if package_type == 'ns':
            artifacts_res = client.nsd_artifacts(user.get_token(), package_id)
        elif package_type == 'vnf':
            artifacts_res = client.vnf_packages_artifacts(user.get_token(), package_id)
        else:
            return False

        files_list = yaml.load(artifacts_res['data'] if artifacts_res and artifacts_res['error'] is False else [])
        result = {'files': files_list}
    except Exception as e:
        log.exception(e)
        result = {'error_msg': 'Unknown error.'}
    return __response_handler(request, result)

@login_required
def custom_action(request, package_id=None, package_type=None, action_name=None):
    if request.method == 'GET':
        return globals()[action_name](request, package_id, package_type)

def __response_handler(request, data_res, url=None, to_redirect=None, *args, **kwargs):
    raw_content_types = request.META.get('HTTP_ACCEPT', '*/*').split(',')
    if 'application/json' in raw_content_types or url is None:
        return HttpResponse(json.dumps(data_res), content_type="application/json", *args, **kwargs)
    elif to_redirect:
        return redirect(url, *args, **kwargs)
    else:
        return render(request, url, data_res)