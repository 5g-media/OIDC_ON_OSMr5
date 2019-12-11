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

from __future__ import unicode_literals

import json
import os.path
import yaml
from lib.util import Util
import logging

from lib.osm.osmclient.client import Client

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('OsmModel.py')


class OsmProject(object):
    """Osm Project class
    """

    @staticmethod
    def get_descriptors( type_descriptor):
        """Returns all descriptors of a given type"""
        log.debug("Get %s descriptors", type_descriptor)
        try:
            client = Client()
            if type_descriptor == 'nsd':
                result = client.nsd_list()

            elif type_descriptor == 'vnfd':
                result = client.vnfd_list()

        except Exception as e:
            log.exception(e)
            result = {}
        return result

    @staticmethod
    def get_descriptor( descriptor_id, type_descriptor):
        """Returns a specific descriptor"""
        try:
            client = Client()
            if type_descriptor == 'nsd':
                result = client.nsd_get(descriptor_id)
                print result
            elif type_descriptor == 'vnfd':
                result = client.vnfd_get(descriptor_id)

                print result
        except Exception as e:
            log.exception(e)
            result = {}

        return result

    @staticmethod
    def get_type():
        return "osm"

    def __str__(self):
        return self.name

    @staticmethod
    def get_overview_data():
        client = Client()
        nsd = client.nsd_list()
        vnfd = client.vnfd_list()
        ns = client.ns_list()
        vnf = client.vnf_list()
        result = {
            'owner': '-',
            'name': '-',
            'updated_date': '-',
            'info': '-',
            'type': 'osm',
            'nsd': len(nsd) if nsd else 0,
            'vnfd': len(vnfd) if vnfd else 0,
            'ns': len(ns) if ns else 0,
            'vnf': len(vnf) if vnf else 0,
        }

        return result

    @staticmethod
    def create_descriptor(descriptor_name, type_descriptor, new_data, data_type, file_uploaded):
        """Creates a descriptor of a given type from a json or yaml representation

        Returns the descriptor id or False
        """
        log.debug('Create descriptor')

        try:
            client = Client()
            if type_descriptor == 'nsd':
                result = client.nsd_onboard(file_uploaded)
            elif type_descriptor == 'vnfd':
                result = client.vnfd_onboard(file_uploaded)

            else:
                log.debug('Create descriptor: Unknown data type')
                return False

        except Exception as e:
            log.exception(e)
            result = False
        return result

    @staticmethod
    def delete_descriptor(type_descriptor, descriptor_id):
        log.debug('Delete descriptor')
        try:
            client = Client()
            if type_descriptor == 'nsd':
                result = client.nsd_delete(descriptor_id)
            elif type_descriptor == 'vnfd':
                result = client.vnfd_delete(descriptor_id)

            else:
                log.debug('Create descriptor: Unknown data type')
                return False

        except Exception as e:
            log.exception(e)
            result = False
        return result

    @staticmethod
    def edit_descriptor(type_descriptor, descriptor_id, new_data, data_type):
        log.debug("Edit descriptor")
        try:
            client = Client()
            if type_descriptor == 'nsd':
                if data_type == 'yaml':
                    new_data = yaml.load(new_data)
                elif data_type == 'json':
                    new_data = json.loads(new_data)
                result = client.nsd_update(descriptor_id, new_data)
            elif type_descriptor == 'vnfd':
                if data_type == 'yaml':
                    new_data = yaml.load(new_data)
                elif data_type == 'json':
                    new_data = json.loads(new_data)
                result = client.vnfd_update(descriptor_id, new_data)

            else:
                log.debug('Create descriptor: Unknown data type')
                return False
        except Exception as e:
            log.exception(e)
            result = False
        return result

    @staticmethod
    def get_package_files_list(type_descriptor, descriptor_id):
        try:
            client = Client()
            if type_descriptor == 'nsd':
                result = client.nsd_artifacts(descriptor_id)
            elif type_descriptor == 'vnfd':
                result = client.vnf_packages_artifacts(descriptor_id)
            else:
                return False
            result = yaml.load(result)
            print result
        except Exception as e:
            log.exception(e)
            result = False
        print result
        return result

    def get_add_element(self, request):
        result = False

        return result

    def get_remove_element(self, request):
        result = False

        return result

    def get_add_link(self, request):

        result = False

        return result

    def get_remove_link(self, request):
        result = False

        return result

    @staticmethod
    def create_ns(descriptor_type, descriptor_id, data_ns):
        try:
            client = Client()
            if descriptor_type == 'nsd':
                result = client.ns_create( data_ns)
            else:
                return False

        except Exception as e:
            log.exception(e)
            result = False
        print result
        return result

    @staticmethod
    def download_pkg(descriptor_id, descriptor_type):
        try:
            client = Client()
            if descriptor_type == 'nsd':
                result = client.get_nsd_pkg(descriptor_id)
            elif descriptor_type == 'vnfd':
                result = client.get_vnfd_pkg(descriptor_id)
            else:
                return False

        except Exception as e:
            log.exception(e)
            result = False
        print result
        return result