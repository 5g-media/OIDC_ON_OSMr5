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
import errno
import requests
import logging
import tarfile
import yaml
import StringIO
from lib.util import Util
import hashlib
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('helper.py')
logging.getLogger("urllib3").setLevel(logging.INFO)


class Client(object):
    def __init__(self):
        self._token_endpoint = 'admin/v1/tokens'
        self._user_endpoint = 'admin/v1/users'
        self._host = os.getenv('OSM_SERVER', "localhost")
        self._so_port = 9999
        self._base_path = 'https://{0}:{1}/osm'.format(self._host, self._so_port)

    def auth(self, args):
        result = {'error': True, 'data': ''}
        token_url = "{0}/{1}".format(self._base_path, self._token_endpoint)
        headers = {"Content-Type": "application/yaml", "accept": "application/json"}
        try:
            r = requests.post(token_url, json=args, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False

        result['data'] = Util.json_loads_byteified(r.text)

        return result

    def switch_project(self, args):
        result = {'error': True, 'data': ''}
        token_url = "{0}/{1}".format(self._base_path, self._token_endpoint)
        headers = {"Content-Type": "application/yaml", "accept": "application/json"}
        try:
            r = requests.post(token_url, json=args, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False

        result['data'] = Util.json_loads_byteified(r.text)

        return result

    def user_list(self, token):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/json", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}

        _url = "{0}/admin/v1/users".format(self._base_path)
        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)

        return result

    def user_create(self, token, user_data):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/json", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}

        _url = "{0}/admin/v1/users".format(self._base_path)

        try:
            r = requests.post(_url, json=user_data, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.created:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)
        return result

    def user_update(self, token, id, user_data):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/json", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}

        _url = "{0}/admin/v1/users/{1}".format(self._base_path, id)
        try:
            r = requests.patch(_url, json=user_data, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.no_content:
            result['error'] = False
        else:
            result['data'] = Util.json_loads_byteified(r.text)
        return result

    def user_delete(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/yaml", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}

        _url = "{0}/admin/v1/users/{1}".format(self._base_path, id)
        try:
            r = requests.delete(_url, params=None, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.no_content:
            result['error'] = False
        else:
            result['data'] = Util.json_loads_byteified(r.text)
        return result

    def get_user_info(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/yaml", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/admin/v1/users/{1}".format(self._base_path, id)
        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)
        return result

    def project_list(self, token):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/yaml", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}

        _url = "{0}/admin/v1/projects".format(self._base_path)
        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)

        return result

    def project_get(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/yaml", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/admin/v1/projects/{1}".format(self._base_path, id)
        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)
        return result

    def project_create(self, token, project_data):

        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/json", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}

        _url = "{0}/admin/v1/projects".format(self._base_path)

        try:
            r = requests.post(_url, json=project_data, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.created:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)
        return result

    def project_edit(self, token, id, project_data):

        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/json", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}

        _url = "{0}/admin/v1/projects/{1}".format(self._base_path, id)

        try:
            r = requests.put(_url, json=project_data, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.no_content:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)
        return result

    def project_delete(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/yaml", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}

        _url = "{0}/admin/v1/projects/{1}".format(self._base_path, id)
        try:
            r = requests.delete(_url, params=None, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.no_content:
            result['error'] = False
        else:
            result['data'] = Util.json_loads_byteified(r.text)
        return result

    def nst_details(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/json", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/nst/v1/netslice_templates/{1}".format(self._base_path,id)
        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)

        return result

    def nst_content(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/json", "accept": "text/plain",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/nst/v1/netslice_templates/{1}/nst".format(self._base_path,id)
        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data']  = Util.json2yaml(yaml.load(str(r.text)))

        return result

    def nst_list(self, token):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/yaml", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        
        _url = "{0}/nst/v1/netslice_templates".format(self._base_path)
        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)

        return result

    def nsd_list(self, token, filter=None):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/yaml", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        query_path = ''
        if filter:
            query_path = '?_admin.type='+filter
        _url = "{0}/nsd/v1/ns_descriptors_content{1}".format(self._base_path, query_path)
        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)

        return result

    def vnfd_list(self, token, filter=None):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/yaml", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        query_path = ''
        if filter:
            query_path = '?_admin.type='+filter
        _url = "{0}/vnfpkgm/v1/vnf_packages_content{1}".format(self._base_path, query_path)
        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)

        return result

    def nsi_list(self, token):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/yaml", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/nsilcm/v1/netslice_instances".format(self._base_path)
        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)

        return result
    
    def ns_list(self, token):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/yaml", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/nslcm/v1/ns_instances_content".format(self._base_path)
        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)

        return result

    def vnf_list(self, token):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/yaml", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/nslcm/v1/vnfrs".format(self._base_path)
        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)

        return result

    def pdu_list(self, token):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/yaml", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/pdu/v1/pdu_descriptors".format(self._base_path)
        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)

        return result

    def nst_delete(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/yaml", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}

        _url = "{0}/nst/v1/netslice_templates/{1}?FORCE=True".format(self._base_path, id)
        try:
            r = requests.delete(_url, params=None, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.no_content:
            result['error'] = False
        
        return result

    def nsd_delete(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/yaml", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}

        _url = "{0}/nsd/v1/ns_descriptors_content/{1}".format(self._base_path, id)
        try:
            r = requests.delete(_url, params=None, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)
        return result

    def vnfd_delete(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/yaml", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}

        _url = "{0}/vnfpkgm/v1/vnf_packages_content/{1}".format(self._base_path, id)
        try:
            r = requests.delete(_url, params=None, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r:
            result['error'] = False
        if r.status_code != requests.codes.no_content:
            result['data'] = Util.json_loads_byteified(r.text)
        return result

    def nst_onboard(self, token, template):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/gzip", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/nst/v1/netslice_templates_content".format(self._base_path)
        try:
            fileName, fileExtension = os.path.splitext(template.name)
            if fileExtension == '.gz':
                headers["Content-Type"] = "application/gzip"
            else:
                headers["Content-Type"] = "application/yaml"
            r = requests.post(_url, data=template, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.created:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)
        return result

    def nsd_onboard(self, token, package):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/gzip", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        with open('/tmp/' + package.name, 'wb+') as destination:
            for chunk in package.chunks():
                destination.write(chunk)
        headers['Content-File-MD5'] = self.md5(open('/tmp/' + package.name, 'rb'))
        _url = "{0}/nsd/v1/ns_descriptors_content/".format(self._base_path)
        try:
            r = requests.post(_url, data=open('/tmp/' + package.name, 'rb'), verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.created:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)
        return result

    def vnfd_onboard(self, token, package):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/gzip", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        with open('/tmp/' + package.name, 'wb+') as destination:
            for chunk in package.chunks():
                destination.write(chunk)
        headers['Content-File-MD5'] = self.md5(open('/tmp/' + package.name, 'rb'))
        _url = "{0}/vnfpkgm/v1/vnf_packages_content".format(self._base_path)
        try:
            r = requests.post(_url, data=open('/tmp/' + package.name, 'rb'), verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.created:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)
        return result

    def nsd_create_pkg_base(self, token, pkg_name):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/gzip", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}

        _url = "{0}/nsd/v1/ns_descriptors_content/".format(self._base_path)

        try:
            self._create_base_pkg('nsd', pkg_name)
            headers['Content-Filename'] = pkg_name + '.tar.gz'
            r = requests.post(_url, data=open('/tmp/' + pkg_name + '.tar.gz', 'rb'), verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.created:
            result['data'] = r.json()
            result['error'] = False
        if r.status_code == requests.codes.conflict:
            result['data'] = "Invalid ID."
        return result

    def vnfd_create_pkg_base(self, token, pkg_name):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/gzip", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}

        _url = "{0}/vnfpkgm/v1/vnf_packages_content".format(self._base_path)

        try:
            self._create_base_pkg('vnfd', pkg_name)
            r = requests.post(_url, data=open('/tmp/' + pkg_name + '.tar.gz', 'rb'), verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.created:
            result['data'] = r.json()
            result['error'] = False
        if r.status_code == requests.codes.conflict:
            result['data'] = "Invalid ID."
        return result

    def nsd_clone(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/gzip", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}

        # get the package onboarded
        tar_pkg = self.get_nsd_pkg(token, id)
        tarf = tarfile.open(fileobj=tar_pkg)
        tarf = self._descriptor_clone(tarf, 'nsd')
        headers['Content-File-MD5'] = self.md5(open('/tmp/' + tarf.getnames()[0] + "_clone.tar.gz", 'rb'))

        _url = "{0}/nsd/v1/ns_descriptors_content/".format(self._base_path)

        try:
            r = requests.post(_url, data=open('/tmp/' + tarf.getnames()[0] + "_clone.tar.gz", 'rb'), verify=False,
                              headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.created:
            result['error'] = False
        if r.status_code == requests.codes.conflict:
            result['data'] = "Invalid ID."

        return result

    def vnfd_clone(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/gzip", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}

        # get the package onboarded
        tar_pkg = self.get_vnfd_pkg(token, id)
        tarf = tarfile.open(fileobj=tar_pkg)

        tarf = self._descriptor_clone(tarf, 'vnfd')
        headers['Content-File-MD5'] = self.md5(open('/tmp/' + tarf.getnames()[0] + "_clone.tar.gz", 'rb'))

        _url = "{0}/vnfpkgm/v1/vnf_packages_content".format(self._base_path)

        try:
            r = requests.post(_url, data=open('/tmp/' + tarf.getnames()[0] + "_clone.tar.gz", 'rb'), verify=False,
                              headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.created:
            result['error'] = False
        if r.status_code == requests.codes.conflict:
            result['data'] = "Invalid ID."

        return result

    def nst_content_update(self, token, id, template):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/yaml", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/nst/v1/netslice_templates/{1}/nst_content".format(self._base_path,id)
        try:
            r = requests.put(_url, data=template, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.no_content:
            result['error'] = False
        return result

    def nsd_update(self, token, id, data):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/gzip", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}

        # get the package onboarded
        tar_pkg = self.get_nsd_pkg(token, id)
        tarf = tarfile.open(fileobj=tar_pkg)

        tarf = self._descriptor_update(tarf, data)
        headers['Content-File-MD5'] = self.md5(open('/tmp/' + tarf.getnames()[0] + ".tar.gz", 'rb'))

        _url = "{0}/nsd/v1/ns_descriptors/{1}/nsd_content".format(self._base_path, id)

        try:
            r = requests.put(_url, data=open('/tmp/' + tarf.getnames()[0] + ".tar.gz", 'rb'), verify=False,
                             headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.no_content:
            result['error'] = False
        else:
            try:
                result['data'] = r.json()
            except Exception as e:
                result['data'] = {}

        return result

    def vnfd_update(self, token, id, data):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/gzip", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}

        # get the package onboarded
        tar_pkg = self.get_vnfd_pkg(token, id)
        tarf = tarfile.open(fileobj=tar_pkg)

        tarf = self._descriptor_update(tarf, data)
        headers['Content-File-MD5'] = self.md5(open('/tmp/' + tarf.getnames()[0] + ".tar.gz", 'rb'))

        _url = "{0}/vnfpkgm/v1/vnf_packages/{1}/package_content".format(self._base_path, id)

        try:
            r = requests.put(_url, data=open('/tmp/' + tarf.getnames()[0] + ".tar.gz", 'rb'), verify=False,
                             headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.no_content:
            result['error'] = False
        else:
            try:
                result['data'] = r.json()
            except Exception as e:
                result['data'] = {}

        return result

    def get_nsd_pkg(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {"accept": "application/zip",
                   'Authorization': 'Bearer {}'.format(token['id'])}

        _url = "{0}/nsd/v1/ns_descriptors/{1}/nsd_content".format(self._base_path, id)
        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
            tarf = StringIO.StringIO(r.content)
            return tarf
        return result

    def get_vnfd_pkg(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {"accept": "application/zip",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/vnfpkgm/v1/vnf_packages/{1}/package_content".format(self._base_path, id)
        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
            tarf = StringIO.StringIO(r.content)
            return tarf
        return result

    def _descriptor_update(self, tarf, data):
        # extract the package on a tmp directory
        tarf.extractall('/tmp')

        for name in tarf.getnames():
            if name.endswith(".yaml") or name.endswith(".yml"):
                with open('/tmp/' + name, 'w') as outfile:
                    yaml.safe_dump(data, outfile, default_flow_style=False)
                break

        tarf_temp = tarfile.open('/tmp/' + tarf.getnames()[0] + ".tar.gz", "w:gz")

        for tarinfo in tarf:
            tarf_temp.add('/tmp/' + tarinfo.name, tarinfo.name, recursive=False)
        tarf_temp.close()
        return tarf

    def _create_base_pkg(self, descriptor_type, pkg_name):
        filename = '/tmp/'+pkg_name+'/' + pkg_name + '.yaml'
        if descriptor_type == 'nsd':
            descriptor = {
                "nsd:nsd-catalog": {
                    "nsd": [
                        {
                            "short-name": str(pkg_name),
                            "vendor": "OSM Composer",
                            "description": str(pkg_name) + " descriptor",
                            "vld": [],
                            "constituent-vnfd": [],
                            "version": "1.0",
                            "id": str(pkg_name),
                            "name": str(pkg_name)
                        }
                    ]
                }
            }

        elif descriptor_type == 'vnfd':
            descriptor = {
                "vnfd:vnfd-catalog": {
                    "vnfd": [
                        {
                            "short-name": str(pkg_name),
                            "vdu": [],
                            "description": "",
                            "mgmt-interface": {
                                "cp": ""
                            },
                            "id": str(pkg_name),
                            "version": "1.0",
                            "internal-vld": [],
                            "connection-point": [],
                            "name": str(pkg_name)
                        }
                    ]
                }
            }

        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open('/tmp/' + pkg_name + '/' + pkg_name + '.yaml', 'w') as yaml_file:
            yaml_file.write(yaml.dump(descriptor, default_flow_style=False))

        tarf_temp = tarfile.open('/tmp/' + pkg_name + '.tar.gz', "w:gz")
        tarf_temp.add('/tmp/'+pkg_name+'/' + pkg_name + '.yaml', pkg_name + '/' + pkg_name + '.yaml', recursive=False)
        tarf_temp.close()

    def _descriptor_clone(self, tarf, descriptor_type):
        # extract the package on a tmp directory
        tarf.extractall('/tmp')

        for name in tarf.getnames():
            if name.endswith(".yaml") or name.endswith(".yml"):
                with open('/tmp/' + name, 'r') as outfile:
                    yaml_object = yaml.load(outfile)

                    if descriptor_type == 'nsd':
                        nsd_list = yaml_object['nsd:nsd-catalog']['nsd']
                        for nsd in nsd_list:
                            nsd['id'] = 'clone_' + nsd['id']
                            nsd['name'] = 'clone_' + nsd['name']
                            nsd['short-name'] = 'clone_' + nsd['short-name']
                    elif descriptor_type == 'vnfd':
                        vnfd_list = yaml_object['vnfd:vnfd-catalog']['vnfd']
                        for vnfd in vnfd_list:
                            vnfd['id'] = 'clone_' + vnfd['id']
                            vnfd['name'] = 'clone_' + vnfd['name']
                            vnfd['short-name'] = 'clone_' + vnfd['short-name']

                    with open('/tmp/' + name, 'w') as yaml_file:
                        yaml_file.write(yaml.dump(yaml_object, default_flow_style=False))
                break

        tarf_temp = tarfile.open('/tmp/' + tarf.getnames()[0] + "_clone.tar.gz", "w:gz")

        for tarinfo in tarf:
            tarf_temp.add('/tmp/' + tarinfo.name, tarinfo.name, recursive=False)
        tarf_temp.close()
        return tarf

    def nsd_get(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {'Content-Type': 'application/yaml',
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/nsd/v1/ns_descriptors/{1}/nsd".format(self._base_path, id)
        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
            return yaml.load(r.text)
        else:
            try:
                result['data'] = r.json()
            except Exception as e:
                result['data'] = {}
        return result

    def vnfd_get(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {'Content-Type': 'application/yaml',
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/vnfpkgm/v1/vnf_packages/{1}/vnfd".format(self._base_path, id)
        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
            return yaml.load(r.text)
        else:
            try:
                result['data'] = r.json()
            except Exception as e:
                result['data'] = {}
        return result

    def nsd_artifacts(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {'Content-Type': 'application/yaml', 'accept': 'text/plain',
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/nsd/v1/ns_descriptors/{1}/artifacts".format(self._base_path, id)
        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
            result['data'] = r.text
        else:
            try:
                result['data'] = r.json()
            except Exception as e:
                result['data'] = {}

        return result

    def vnf_packages_artifacts(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {'Content-Type': 'application/yaml', 'accept': 'text/plain',
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/vnfpkgm/v1/vnf_packages/{1}/artifacts".format(self._base_path, id)
        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
            result['data'] = r.text
        else:
            try:
                result['data'] = r.json()
            except Exception as e:
                result['data'] = {}

        return result

    def nsi_create(self, token, nsi_data):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/yaml", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}

        _url = "{0}/nsilcm/v1/netslice_instances_content".format(self._base_path)

        try:
            r = requests.post(_url, json=nsi_data, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)
        return result

    def ns_create(self, token, ns_data):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/yaml", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}

        _url = "{0}/nslcm/v1/ns_instances_content".format(self._base_path)

        try:
            r = requests.post(_url, json=ns_data, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)
        return result

    def pdu_create(self, token, pdu_data):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/yaml", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}

        _url = "{0}/pdu/v1/pdu_descriptors".format(self._base_path)

        try:
            r = requests.post(_url, json=pdu_data, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.created:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)
        return result

    def ns_op_list(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/json", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/nslcm/v1/ns_lcm_op_occs/?nsInstanceId={1}".format(self._base_path, id)

        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)

        return result

    def nsi_op_list(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/json", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/nsilcm/v1/nsi_lcm_op_occs/?nsInstanceId={1}".format(self._base_path, id)

        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)

        return result

    def ns_op(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/json", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/nslcm/v1/ns_lcm_op_occs/{1}".format(self._base_path, id)

        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)

        return result

    def ns_action(self, token, id, action_payload):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/json", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}

        _url = "{0}/nslcm/v1/ns_instances/{1}/action".format(self._base_path, id)

        try:
            r = requests.post(_url, json=action_payload, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.created:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)
        return result

    def nsi_delete(self, token, id, force=None):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/yaml", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        query_path = ''
        if force:
            query_path = '?FORCE=true'
        _url = "{0}/nsilcm/v1/netslice_instances_content/{1}{2}".format(self._base_path, id, query_path)
        try:
            r = requests.delete(_url, params=None, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r:
            result['error'] = False
        if r.status_code != requests.codes.no_content:
            result['data'] = Util.json_loads_byteified(r.text)
        return result

    def ns_delete(self, token, id, force=None):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/yaml", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        query_path = ''
        if force:
            query_path = '?FORCE=true'
        _url = "{0}/nslcm/v1/ns_instances_content/{1}{2}".format(self._base_path, id, query_path)
        try:
            r = requests.delete(_url, params=None, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r:
            result['error'] = False
        if r.status_code != requests.codes.no_content:
            result['data'] = Util.json_loads_byteified(r.text)
        return result

    def pdu_delete(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/yaml", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/pdu/v1/pdu_descriptors/{1}".format(self._base_path, id)
        try:
            r = requests.delete(_url, params=None, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r:
            result['error'] = False
        if r.status_code != requests.codes.no_content:
            result['data'] = Util.json_loads_byteified(r.text)
        return result

    def nsi_get(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/json", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/nsilcm/v1/netslice_instances/{1}".format(self._base_path, id)

        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)
        return result

    def ns_get(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/json", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/nslcm/v1/ns_instances_content/{1}".format(self._base_path, id)

        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)
        return result

    def vnf_get(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/json", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/nslcm/v1/vnfrs/{1}".format(self._base_path, id)

        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)
        return result

    def pdu_get(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/json", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/pdu/v1/pdu_descriptors/{1}".format(self._base_path, id)

        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)
        return result

    def ns_alarm_create(self, token, id, alarm_payload):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/test/message/alarm_request".format(self._base_path)
        try:
            r = requests.post(_url, json=alarm_payload, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        # result['data'] = Util.json_loads_byteified(r.text)
        result['data'] = r.text
        return result

    def ns_metric_export(self, token, id, metric_payload):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/test/message/metric_request".format(self._base_path)
        try:
            r = requests.post(_url, json=metric_payload, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        # result['data'] = Util.json_loads_byteified(r.text)
        result['data'] = r.text
        return result

    def vim_list(self, token):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/yaml", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/admin/v1/vims".format(self._base_path)
        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)

        return result

    def vim_delete(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {"accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/admin/v1/vims/{1}".format(self._base_path, id)
        try:
            r = requests.delete(_url, params=None, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.accepted:
            result['error'] = False
        else:
            result['data'] = r.text
        return result

    def vim_get(self, token, id):

        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/json", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/admin/v1/vims/{1}".format(self._base_path, id)

        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)
        return result

    def vim_create(self, token, vim_data):

        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/json", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}

        _url = "{0}/admin/v1/vims".format(self._base_path)

        try:
            r = requests.post(_url, json=vim_data, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.created:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)
        return result

    def sdn_list(self, token):
        result = {'error': True, 'data': ''}
        headers = {"accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/admin/v1/sdns".format(self._base_path)
        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)
        return result

    def sdn_delete(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {"accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/admin/v1/sdns/{1}".format(self._base_path, id)
        try:
            r = requests.delete(_url, params=None, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.accepted:
            result['error'] = False
        else:
            result['data'] = r.text
        return result

    def sdn_get(self, token, id):
        result = {'error': True, 'data': ''}
        headers = {"accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}
        _url = "{0}/admin/v1/sdns/{1}".format(self._base_path, id)

        try:
            r = requests.get(_url, params=None, verify=False, stream=True, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.ok:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)
        return result

    def sdn_create(self, token, sdn_data):
        result = {'error': True, 'data': ''}
        headers = {"Content-Type": "application/json", "accept": "application/json",
                   'Authorization': 'Bearer {}'.format(token['id'])}

        _url = "{0}/admin/v1/sdns".format(self._base_path)

        try:
            r = requests.post(_url, json=sdn_data, verify=False, headers=headers)
        except Exception as e:
            log.exception(e)
            result['data'] = str(e)
            return result
        if r.status_code == requests.codes.created:
            result['error'] = False
        result['data'] = Util.json_loads_byteified(r.text)
        return result

    @staticmethod
    def md5(f):
        hash_md5 = hashlib.md5()
        for chunk in iter(lambda: f.read(1024), b""):
            hash_md5.update(chunk)
        return hash_md5.hexdigest()
