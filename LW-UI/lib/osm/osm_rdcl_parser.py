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


import logging
# from lib.rdcl_graph import RdclGraph
import copy

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('OsmParser')


class RdclGraph(object):
    """ Operates on the graph representation used for the GUI graph views """
    node_ids = []
    node_t3d_base = {
        'info': {
            'property': {
                'custom_label': '',
            },
            'type': '',
            'group': []
        }
    }

    def __init__(self):
        pass

    def add_link(self, source, target, view, group, graph_object, optional={}):
        if (source is None or source not in self.node_ids) or (target is None or target not in self.node_ids):
            return
        edge_obj = {
            'source': source,
            'target': target,
            'view': view,
            'group': [group],
        }

        edge_obj.update(optional)
        #if edge_obj not in graph_object['edges']:
        #    graph_object['edges'].append(edge_obj)
        graph_object['edges'].append(edge_obj)

    def add_node(self, id, type, group, positions, graph_object, optional={}):
        if id is None:
            return
        node = next((x for x in graph_object['vertices'] if x['id'] == id), None)
        if node is not None:
            node['info']['group'].append(group)
        else:
            node = copy.deepcopy(self.node_t3d_base)
            node['id'] = id
            node['info']['type'] = type
            if group is not None:
                node['info']['group'].append(group)
            if positions and id in positions['vertices'] and 'x' in positions['vertices'][id] and 'y' in \
                    positions['vertices'][id]:
                node['fx'] = positions['vertices'][id]['x']
                node['fy'] = positions['vertices'][id]['y']
            node['info'].update(optional)
            graph_object['vertices'].append(node)
            self.node_ids.append(id)

    def is_directed_edge(self, source_type=None, target_type=None, layer=None, model={}):
        if source_type is None or target_type is None or layer is None:
            return None
        if layer in model['layer'] and 'allowed_edges' in model['layer'][layer]:
            if source_type in model['layer'][layer]['allowed_edges'] and target_type in \
                    model['layer'][layer]['allowed_edges'][source_type]['destination']:
                edge_pro = model['layer'][layer]['allowed_edges'][source_type]['destination'][target_type]
                return edge_pro['direct_edge'] if 'direct_edge' in edge_pro else False

        return None


class OsmParser(RdclGraph):
    """ Operates on the graph representation used for the GUI graph views """

    def nsr_to_graph(self, nsr_full):

        graph = {'vertices': [], 'edges': [], 'model': {
            "layer": {

                "nsr": {
                    "nodes": {
                        "vnfr": {
                            "addable": {},
                            "removable": {},
                            "expands": "vnfr"
                        },
                        "ns_vl": {
                            "addable": {},
                            "removable": {}
                        },
                        "ns_cp": {
                            "addable": {},
                            "removable": {}
                        },

                    },
                    "allowed_edges": {
                        "ns_vl": {
                            "destination": {
                                "vnfr": {
                                    "callback": "addLink",
                                    "direct_edge": False,
                                    "removable": {}
                                }
                            }
                        },
                        "vnfr": {
                            "destination": {
                                "ns_vl": {
                                    "callback": "addLink",
                                    "direct_edge": False,
                                    "removable": {}
                                },

                            }
                        }

                    }
                },

                "vnfr": {
                    "nodes": {
                        "vdur": {},
                        "cp": {},
                        "int_cp": {},
                        "vnf_vl": {}

                    },
                    "allowed_edges": {
                        "vdur": {
                            "destination": {
                                "cp": {
                                    "direct_edge": False,
                                },
                                "int_cp": {
                                    "direct_edge": False,
                                },
                                "vnf_vl": {
                                    "direct_edge": False,
                                }
                            }
                        },
                        "cp": {
                            "destination": {
                                "vdur": {
                                    "direct_edge": False,
                                }
                            }
                        },
                        "int_cp": {
                            "destination": {
                                "vdur": {
                                    "direct_edge": False,
                                },
                                "vnf_vl": {
                                    "direct_edge": False,
                                }
                            }
                        },
                        "vnf_vl": {
                            "destination": {
                                "vdur": {
                                    "direct_edge": False
                                }
                            }
                        }
                    }
                },
                "name": "OSM",
                "version": 1,
                "description": "osm"
            }
        }, 'graph_parameters': {'view': {'nsr': {}, 'vnfr': {}}}}

        nsr = nsr_full['nsr']

        graph['graph_parameters']['view']['nsr'] = {}
        nsr_graph_param = graph['graph_parameters']['view']['nsr']
        nsr_graph_param['id'] = nsr['_id'] if '_id' in nsr else None
        nsr_graph_param['nsdId'] = nsr['nsdId'] if 'nsdId' in nsr else None
        nsr_graph_param['name-ref'] = nsr['name-ref'] if 'name-ref' in nsr else None
        nsr_graph_param['operational-status'] = nsr['operational-status'] if 'operational-status' in nsr else None
        nsr_graph_param['config-status'] = nsr['config-status'] if 'config-status' in nsr else None
        nsr_graph_param['detailed-status'] = nsr['detailed-status'] if 'detailed-status' in nsr else None
        nsr_graph_param['create-time'] = nsr['create-time'] if 'create-time' in nsr else None
        nsr_graph_param['instantiate_params'] = nsr['instantiate_params'] if 'instantiate_params' in nsr else None

        map_vnf_index_to_id = {}
        for vnfr_id in nsr['constituent-vnfr-ref']:
            current_vnfr = nsr_full['vnfr'][vnfr_id]

            graph['graph_parameters']['view']['vnfr'][vnfr_id] = {}
            vnfr_graph_param = graph['graph_parameters']['view']['vnfr'][vnfr_id]
            vnfr_graph_param['id'] = vnfr_id
            vnfr_graph_param['vnfd-id'] = current_vnfr['vnfd-id']
            vnfr_graph_param['vnfd-ref'] = current_vnfr['vnfd-ref']
            vnfr_graph_param['member-vnf-index-ref'] = current_vnfr['member-vnf-index-ref']
            vnfr_graph_param['vim-account-id'] = current_vnfr['vim-account-id']
            vnfr_graph_param['created-time'] = current_vnfr['created-time']

            vnfr_label = current_vnfr['vnfd-ref'] + ':' + current_vnfr['member-vnf-index-ref']
            map_vnf_index_to_id[current_vnfr['member-vnf-index-ref']] = vnfr_id
            self.add_node(vnfr_id, 'vnfr', None, None, graph,
                          {'property': {'custom_label': vnfr_label}, 'osm': current_vnfr})

            for cp in current_vnfr['connection-point']:
                if cp['id']:
                    cp_id = vnfr_label + ':' + cp['id']
                    self.add_node(cp_id, 'cp', vnfr_id, None, graph, {'osm': cp})

            for vdur in current_vnfr['vdur']:
                vdur_id = vnfr_label + ':' + vdur['vdu-id-ref']
                self.add_node(vdur_id, 'vdur', vnfr_id, None, graph, {'osm': vdur})
                if current_vnfr['vnfd-id'] in nsr_full['vnfd']:
                    for vdu in nsr_full['vnfd'][current_vnfr['vnfd-id']]['vdu']:
                        if vdu['id'] == vdur['vdu-id-ref']:
                            if 'internal-connection-point' in vdu:
                                for int_cp in vdu['internal-connection-point']:
                                    cp_id = vnfr_label + ':' + int_cp['id']
                                    self.add_node(cp_id, 'int_cp', vnfr_id, None, graph, {'osm': int_cp})
                            for interface in vdu['interface']:
                                if interface['type'] == "EXTERNAL":
                                    cp_id = vnfr_label + ':' + interface['external-connection-point-ref']
                                    self.add_link(cp_id, vdur_id, 'vnfr', vnfr_id, graph)
                                elif interface['type'] == "INTERNAL":
                                    cp_id = vnfr_label + ':' + interface['internal-connection-point-ref']
                                    self.add_link(cp_id, vdur_id, 'vnfr', vnfr_id, graph)

            if current_vnfr['vnfd-id'] in nsr_full['vnfd'] and 'internal-vld' in nsr_full['vnfd'][
                current_vnfr['vnfd-id']]:
                for vnfd_vld in nsr_full['vnfd'][current_vnfr['vnfd-id']]['internal-vld']:
                    vld_id = vnfr_label + ':' + vnfd_vld['id']
                    self.add_node(vld_id, 'vnf_vl', vnfr_id, None, graph, {'osm': vnfd_vld})
                    if vnfd_vld['internal-connection-point']:
                        for int_cp in vnfd_vld['internal-connection-point']:
                            int_cp_id = vnfr_label + ':' + int_cp['id-ref']
                            self.add_link(vld_id, int_cp_id, 'vnfr', vnfr_id, graph)

        for ns_vld in nsr['nsd']['vld']:
            self.add_node(ns_vld['id'], 'ns_vl', None, None, graph,
                          {'property': {'custom_label': ns_vld['name']}, 'osm': ns_vld})
            for cp_ref in ns_vld['vnfd-connection-point-ref']:
                ns_vld['id']+ ':' + str(cp_ref['member-vnf-index-ref']) + ':' + cp_ref['vnfd-connection-point-ref']
                cp_id = ns_vld['id']+ ':' + str(cp_ref['member-vnf-index-ref']) + ':' + cp_ref['vnfd-connection-point-ref']             
                cp_label = str(cp_ref['vnfd-connection-point-ref'])
                self.add_node(cp_id,'ns_cp','nsd',None,graph, {'property': {'custom_label': cp_label}, 'osm': cp_ref})
                self.add_link(cp_id, ns_vld['id'], 'nsr', None, graph)
                self.add_link(cp_id, map_vnf_index_to_id[str(cp_ref['member-vnf-index-ref'])], 'nsr', None, graph)

        return graph

    def vnfd_to_graph(self, vnfd_catalog):
        graph = {'vertices': [], 'edges': [], 'model': {
            "layer": {
                "vnfd": {
                    "nodes": {
                        "vdu": {
                            "addable": {
                                "callback": "addNode"
                            },
                            "removable": {
                                "callback": "removeNode"
                            }
                        },
                        "cp": {
                            "addable": {
                                "callback": "addNode"
                            },
                            "removable": {
                                "callback": "removeNode"
                            }
                        },
                        "int_cp": {
                            "removable": {
                                "callback": "removeNode"
                            }
                        },
                        "vnf_vl": {
                            "addable": {
                                "callback": "addNode"
                            },
                            "removable": {
                                "callback": "removeNode"
                            }
                        }
                    },
                    "allowed_edges": {
                        "vdu": {
                            "destination": {
                                "cp": {
                                    "callback": "addLink",
                                    "direct_edge": False,
                                    "removable": {}
                                },
                                "vnf_vl": {
                                    "callback": "addLink",
                                    "direct_edge": False,
                                    "removable": {}
                                }
                            }
                        },
                        "cp": {
                            "destination": {
                                "vdu": {
                                    "callback": "addLink",
                                    "direct_edge": False,
                                    "removable": {}
                                }
                            }
                        },
                        # "int_cp": {
                        #     "destination": {
                        #         "vdu": {
                        #             "direct_edge": False,
                        #         },
                        #         "vnf_vl": {
                        #             "direct_edge": False,
                        #         }
                        #     }
                        # },
                        "vnf_vl": {
                            "destination": {
                                "int_cp": {
                                    "direct_edge": False
                                },
                                "vdu": {
                                    "callback": "addLink",
                                    "direct_edge": False,
                                    "removable": {}
                                }
                            }
                        }
                    }
                },
                "name": "OSM",
                "version": 1,
                "description": "osm"
            }, "callback": {"addNode": {"class": "OSMController"}, "removeNode": {"class": "OSMController"},
                            "removeLink": {"class": "OSMController"}, "addLink": {"class": "OSMController"}}
        }, 'graph_parameters': {'view': {'vnfd': {}}}}
        if 'vnfd-catalog' in vnfd_catalog:
            vnfd = vnfd_catalog['vnfd-catalog']['vnfd'][0]
        elif 'vnfd:vnfd-catalog' in vnfd_catalog:
            vnfd = vnfd_catalog['vnfd:vnfd-catalog']['vnfd'][0]
        else:
            return graph
        vnfd_graph_param = graph['graph_parameters']['view']['vnfd']
        vnfd_graph_param['id'] = vnfd['id'] if 'id' in vnfd else None
        vnfd_graph_param['name'] = vnfd['name'] if 'name' in vnfd else None
        vnfd_graph_param['short-name'] = vnfd['short-name'] if 'short-name' in vnfd else None
        vnfd_graph_param['description'] = vnfd['description'] if 'description' in vnfd else None
        vnfd_graph_param['version'] = vnfd['version'] if 'version' in vnfd else None
        vnfd_graph_param['vendor'] = vnfd['vendor'] if 'vendor' in vnfd else None
        if 'connection-point' in vnfd:
            for extCp in vnfd['connection-point']:
                self.add_node(extCp['name'], 'cp', vnfd['id'], None, graph,
                              {'property': {'custom_label': extCp['name']}, 'osm': extCp})
        if 'vdu' in vnfd:
            for vdu in vnfd['vdu']:
                self.add_node(vdu['id'], 'vdu', vnfd['id'], None, graph,
                              {'property': {'custom_label': vdu['id']}, 'osm': vdu})
                if 'internal-connection-point' in vdu:
                    for intCp in vdu['internal-connection-point']:
                        self.add_node(intCp['id'], 'int_cp', vnfd['id'], None, graph,
                                      {'property': {'custom_label': intCp['id']}, 'osm': intCp})
                if 'interface' in vdu:
                    for interface in vdu['interface']:
                        if interface['type'] == "EXTERNAL":
                            self.add_link(vdu['id'], interface['external-connection-point-ref'], 'vnfd', vnfd['id'], graph)
                        elif interface['type'] == "INTERNAL":
                            self.add_link(vdu['id'], interface['internal-connection-point-ref'], 'vnfd', vnfd['id'], graph, {'short': True})
        if 'internal-vld' in vnfd:
            for intVl in vnfd['internal-vld']:
                self.add_node(intVl['id'], 'vnf_vl', intVl['id'], None, graph,
                              {'property': {'custom_label': intVl['id']}, 'osm': intVl})
                for intCp in intVl['internal-connection-point']:
                    self.add_link(intVl['id'], intCp['id-ref'], 'vnfd', vnfd['id'], graph)

        return graph

    def nsd_to_graph(self, nsd_catalog):
        graph = {'vertices': [], 'edges': [], 'model': {
            "layer": {
                "nsd": {
                    "nodes": {
                        "vnf": {
                            "addable": {"callback": "addNode"},
                            "removable": {"callback": "removeNode"}
                        },
                        "ns_cp": {
                            "removable": {"callback": "removeNode"}
                        },
                        "ns_vl": {
                            "addable": {
                                "callback": "addNode"
                            },
                            "removable": {
                                "callback": "removeNode"
                            }
                        }
                    },
                    "allowed_edges": {
                        "vnf":{
                            "destination": {
                                "ns_cp": {
                                    "direct_edge": False,
                                    "removable" : {
                                        "callback": "removeLink",
                                    }
                                },
                                "ns_vl": {
                                    "direct_edge": False,
                                    "callback": "addLink",
                                }
                            }
                        },
                        "ns_vl": {
                            "destination": {
                                "ns_cp": {
                                    "direct_edge": False,
                                    "removable": {
                                        "callback": "removeLink",
                                    }
                                },
                                "vnf": {
                                    "direct_edge": False,
                                    "callback": "addLink",
                                }
                            }
                        },
                        "ns_cp": {
                            "destination": {
                                "ns_vl": {
                                    "direct_edge": False,
                                    "removable": {
                                        "callback": "removeLink",
                                    }
                                },
                                "vnf": {
                                    "direct_edge": False,
                                    "removable": {
                                        "callback": "removeLink",
                                    }
                                }
                            }
                        }
                    }
                },
                "vnfd": {
                    "nodes": {
                        "vdu": {},
                        "cp": {},
                        "int_cp": {},
                        "vnf_vl": {}
                    },
                    "allowed_edges": {
                        "vdu": {
                            "destination": {
                                "cp": {
                                    "direct_edge": False,
                                },
                                "int_cp": {
                                    "direct_edge": False,
                                },
                                "vnf_vl": {
                                    "direct_edge": False,
                                }
                            }
                        },
                        "cp": {
                            "destination": {
                                "vdu": {
                                    "direct_edge": False,
                                }
                            }
                        },
                        "int_cp": {
                            "destination": {
                                "vdu": {
                                    "direct_edge": False,
                                },
                                "vnf_vl": {
                                    "direct_edge": False,
                                }
                            }
                        },
                        "vnf_vl": {
                            "destination": {
                                "vdu": {
                                    "direct_edge": False
                                }
                            }
                        }
                    }
                },
                "name": "OSM",
                "version": 1,
                "description": "osm"
            }, "callback": {"addNode": {"class": "OSMController"}, "removeNode": {"class": "OSMController"},
                            "removeLink": {"class": "OSMController"}, "addLink": {"class": "OSMController"}}
        }, 'graph_parameters': {'view': {'nsd': {}}}}
        if 'nsd-catalog' in nsd_catalog:
            nsd = nsd_catalog['nsd-catalog']['nsd'][0]
        elif 'nsd:nsd-catalog' in nsd_catalog:
            nsd = nsd_catalog['nsd:nsd-catalog']['nsd'][0]
        else:
            return graph

        nsd_graph_param = graph['graph_parameters']['view']['nsd']
        nsd_graph_param['id'] = nsd['id'] if 'id' in nsd else None
        nsd_graph_param['name'] = nsd['name'] if 'name' in nsd else None
        nsd_graph_param['short-name'] = nsd['short-name'] if 'short-name' in nsd else None
        nsd_graph_param['description'] = nsd['description'] if 'description' in nsd else None
        nsd_graph_param['version'] = nsd['version'] if 'version' in nsd else None
        nsd_graph_param['vendor'] = nsd['vendor'] if 'vendor' in nsd else None

        if 'constituent-vnfd' in nsd:
            for vnfd in nsd['constituent-vnfd']:
                costinuent_id = vnfd['vnfd-id-ref']+":"+str(vnfd['member-vnf-index'])
                self.add_node(costinuent_id, 'vnf', None, None, graph,
                              {'property': {'custom_label': costinuent_id}, 'osm': vnfd})

        if 'vld' in nsd:
            for vld in nsd['vld']:
                self.add_node(vld['id'], 'ns_vl', None, None, graph,
                              {'property': {'custom_label': vld['id']}, 'osm': vld})
                if 'vnfd-connection-point-ref' in vld:
                    for cp_ref in vld['vnfd-connection-point-ref']:
                        vnfd_id = cp_ref['vnfd-id-ref'] + ':' + str(cp_ref['member-vnf-index-ref'])
                        cp_id = vld['id']+ ':' + str(cp_ref['member-vnf-index-ref']) + ':' + cp_ref['vnfd-connection-point-ref']
                        cp_label = vld['id']+ ':' + cp_ref['vnfd-connection-point-ref']
                        node_payload = {'vld_id': vld['id']}
                        node_payload.update(cp_ref)
                        self.add_node(cp_id,'ns_cp',None,None,graph,
                        {'property': {'custom_label': cp_label}, 'osm': node_payload})
                        
                        self.add_link(cp_id, vld['id'], 'nsd', None, graph)
                        self.add_link(cp_id, vnfd_id, 'nsd', None, graph)
        return graph


if __name__ == '__main__':
    parser = OsmParser()
    print parser.nsr_to_graph({})
