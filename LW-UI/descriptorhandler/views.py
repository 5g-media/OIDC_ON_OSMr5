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
log = logging.getLogger('descriptorhandler/view.py')


@login_required
def addElement(request, descriptor_type=None, descriptor_id=None, element_type=None):
    user = osmutils.get_user(request)
    client = Client()
    if descriptor_type == 'nsd':
        descriptor_result = client.nsd_get(user.get_token(), descriptor_id)
        element_id = request.POST.get('id', '')
        util = OsmUtil()
        descriptor_updated = util.add_base_node('nsd', descriptor_result, element_type, element_id, request.POST.dict())
        result = client.nsd_update(user.get_token(), descriptor_id, descriptor_updated)
        if result['error'] == True:
            return __response_handler(request, result['data'], url=None,
                                      status=result['data']['status'] if 'status' in result['data'] else 500)
        else:
            parser = OsmParser()
            # print nsr_object
            if descriptor_type == 'nsd':
                result_graph = parser.nsd_to_graph(descriptor_updated)

        return __response_handler(request, result_graph, url=None, status=200)

    elif descriptor_type == 'vnfd':
        descriptor_result = client.vnfd_get(user.get_token(), descriptor_id)
        element_id = request.POST.get('id', '')
        util = OsmUtil()
        descriptor_updated = util.add_base_node('vnfd', descriptor_result, element_type, element_id, request.POST.dict())
        result = client.vnfd_update(user.get_token(), descriptor_id, descriptor_updated)
        if result['error'] == True:
            return __response_handler(request, result['data'], url=None,
                                      status=result['data']['status'] if 'status' in result['data'] else 500)
        else:
            parser = OsmParser()
            # print nsr_object
            if descriptor_type == 'vnfd':
                result_graph = parser.vnfd_to_graph(descriptor_updated)

        return __response_handler(request, result_graph, url=None, status=200)


@login_required
def removeElement(request, descriptor_type=None, descriptor_id=None, element_type=None):
    user = osmutils.get_user(request)
    client = Client()
    if descriptor_type == 'nsd':
        descriptor_result = client.nsd_get(user.get_token(), descriptor_id)
        element_id = request.POST.get('id', '')
        util = OsmUtil()
        descriptor_updated = util.remove_node('nsd', descriptor_result, element_type, element_id, request.POST.dict())
        result = client.nsd_update(user.get_token(), descriptor_id, descriptor_updated)
        if result['error'] == True:
            return __response_handler(request, result['data'], url=None,
                                      status=result['data']['status'] if 'status' in result['data'] else 500)
        else:
            parser = OsmParser()
            # print nsr_object
            if descriptor_type == 'nsd':
                result_graph = parser.nsd_to_graph(descriptor_updated)

        return __response_handler(request, result_graph, url=None, status=200)

    elif descriptor_type == 'vnfd':
        descriptor_result = client.vnfd_get(user.get_token(), descriptor_id)
        element_id = request.POST.get('id', '')
        util = OsmUtil()
        descriptor_updated = util.remove_node('vnfd', descriptor_result, element_type, element_id, request.POST.dict())
        result = client.vnfd_update(user.get_token(), descriptor_id, descriptor_updated)
        if result['error'] == True:
            return __response_handler(request, result['data'], url=None,
                                      status=result['data']['status'] if 'status' in result['data'] else 500)
        else:
            parser = OsmParser()
            # print nsr_object
            if descriptor_type == 'vnfd':
                result_graph = parser.vnfd_to_graph(descriptor_updated)

            return __response_handler(request, result_graph, url=None, status=200)


@login_required
def updateElement(request, descriptor_type=None, descriptor_id=None, element_type=None):
    user = osmutils.get_user(request)
    client = Client()
    payload = request.POST.dict()
    util = OsmUtil()

    if descriptor_type == 'nsd':
        descriptor_result = client.nsd_get(user.get_token(), descriptor_id)
    elif descriptor_type == 'vnfd':
        descriptor_result = client.vnfd_get(user.get_token(), descriptor_id)
    
    if element_type == 'graph_params':
        descriptor_updated = util.update_graph_params(descriptor_type, descriptor_result, json.loads(payload['update']))
    else:
        descriptor_updated = util.update_node(descriptor_type, descriptor_result, element_type, json.loads(payload['old']), json.loads(payload['update']))

    if descriptor_type == 'nsd':
        result = client.nsd_update(user.get_token(), descriptor_id, descriptor_updated)
    elif descriptor_type == 'vnfd':
        result = client.vnfd_update(user.get_token(), descriptor_id, descriptor_updated)
    if result['error'] == True:
            return __response_handler(request, result['data'], url=None,
                                      status=result['data']['status'] if 'status' in result['data'] else 500)
    else:
        parser = OsmParser()
        if descriptor_type == 'vnfd':
            result_graph = parser.vnfd_to_graph(descriptor_updated)
        elif descriptor_type == 'nsd':
            result_graph = parser.nsd_to_graph(descriptor_updated)
        return __response_handler(request, result_graph, url=None, status=200)



@login_required
def edit_descriptor(request, descriptor_id=None, descriptor_type=None):
    user = osmutils.get_user(request)
    project_id = user.project_id
    if request.method == 'POST':
        new_data = request.POST.get('text'),
        data_type = request.POST.get('type')
        #print new_data
        try:
            client = Client()
            if descriptor_type == 'nsd':
                if data_type == 'yaml':
                    new_data = yaml.load(request.POST.get('text'))
                elif data_type == 'json':
                    new_data = json.loads(request.POST.get('text'))
                result = client.nsd_update(user.get_token(), descriptor_id, new_data)
            elif descriptor_type == 'vnfd':
                if data_type == 'yaml':
                    new_data = yaml.load(request.POST.get('text'))
                elif data_type == 'json':
                    new_data = json.loads(request.POST.get('text'))
                result = client.vnfd_update(user.get_token(), descriptor_id, new_data)

            else:
                log.debug('Update descriptor: Unknown data type')
                result = {'error': True, 'data': 'Update descriptor: Unknown data type'}
        except Exception as e:
            log.exception(e)
            result = {'error': True, 'data': str(e)}
        if result['error'] == True:
            return __response_handler(request, result['data'], url=None, status=result['data']['status'] if 'status' in result['data'] else 500)
        else:
            return __response_handler(request, {}, url=None, status=200)

    elif request.method == 'GET':

        page = 'descriptor_view.html'
        try:
            client = Client()
            if descriptor_type == 'nsd':
                result = client.nsd_get(user.get_token(), descriptor_id)
            elif descriptor_type == 'vnfd':
                result = client.vnfd_get(user.get_token(), descriptor_id)
        except Exception as e:
            log.exception(e)
            result = {'error': True, 'data': str(e)}

        if isinstance(result, dict) and 'error' in result and result['error']:
            return render(request, 'error.html')

        descriptor_string_json = json.dumps(result, indent=2)
        descriptor_string_yaml = Util.json2yaml(result)
        # print descriptor
        return render(request, page, {
            'project_id': project_id,
            'descriptor_id': descriptor_id,
            'descriptor_type': descriptor_type,
            'descriptor_strings': {'descriptor_string_yaml': descriptor_string_yaml,
                                   'descriptor_string_json': descriptor_string_json}})

@login_required
def open_composer(request):
    user = osmutils.get_user(request)
    descriptor_id = request.GET.get('id')
    descriptor_type = request.GET.get('type')
    result = {}
    client = Client()
    if descriptor_id:
        raw_content_types = request.META.get('HTTP_ACCEPT', '*/*').split(',')
        if 'application/json' not in raw_content_types:
            return __response_handler(request, {'type': descriptor_type}, 'composer.html')
        try:
            if descriptor_type == 'nsd':
                descriptor_result = client.nsd_get(user.get_token(), descriptor_id)
            elif descriptor_type == 'vnfd':
                descriptor_result = client.vnfd_get(user.get_token(), descriptor_id)

        except Exception as e:
            descriptor_result = {'error': True, 'data': str(e)}

        if isinstance(descriptor_result, dict) and 'error' in descriptor_result and descriptor_result['error']:
            return render(request, 'error.html')

        test = OsmParser()
        # print nsr_object
        if descriptor_type == 'nsd':
            result = test.nsd_to_graph(descriptor_result)
        elif descriptor_type == 'vnfd':
            result = test.vnfd_to_graph(descriptor_result)
        return __response_handler(request, result, 'composer.html')

    return __response_handler(request, result, 'composer.html')

def get_available_nodes(request):
    user = osmutils.get_user(request)
    params = request.GET.dict()
    client = Client()
    result = []
    try:
        if params['layer'] == 'nsd':
            descriptors = client.vnfd_list(user.get_token())
    except Exception as e:
        log.exception(e)
        descriptors = []
    if descriptors and descriptors['error'] is False:
        for desc in descriptors['data']:
            # print desc
            result.append({'_id': desc['_id'],'id': desc['id'], 'name': desc['short-name']})

    return __response_handler(request, {'descriptors': result})

@login_required
def custom_action(request, descriptor_id=None, descriptor_type=None, action_name=None):
    if request.method == 'GET':
        return globals()[action_name](request, descriptor_id, descriptor_type)

def __response_handler(request, data_res, url=None, to_redirect=None, *args, **kwargs):
    raw_content_types = request.META.get('HTTP_ACCEPT', '*/*').split(',')
    if 'application/json' in raw_content_types or url is None:
        return HttpResponse(json.dumps(data_res), content_type="application/json", *args, **kwargs)
    elif to_redirect:
        return redirect(url, *args, **kwargs)
    else:
        return render(request, url, data_res)
