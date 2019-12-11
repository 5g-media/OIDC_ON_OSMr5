class OsmUtil():

    @staticmethod
    def remove_node(descriptor_type, descriptor, node_type, element_id, args):
        if descriptor_type == 'nsd':
            if 'nsd-catalog' in descriptor:
                nsd = descriptor['nsd-catalog']['nsd'][0]
            elif 'nsd:nsd-catalog' in descriptor:
                nsd = descriptor['nsd:nsd-catalog']['nsd'][0]

            if node_type == 'ns_vl':
                for k, v in enumerate(nsd['vld']):
                    if v['id'] == args['id']:
                        nsd['vld'].pop(k)
            elif node_type == 'vnf':
                for k, v in enumerate(nsd['constituent-vnfd']):
                    if str(v['member-vnf-index']) == str(args['member-vnf-index']) and str(v['vnfd-id-ref']) == str(
                            args['vnfd-id-ref']):
                        nsd['constituent-vnfd'].pop(k)
                        for j, vld in enumerate(nsd['vld']):
                            vld['vnfd-connection-point-ref'] = [item for item in vld['vnfd-connection-point-ref'] if
                                                                str(item['member-vnf-index-ref']) != str(
                                                                    args['member-vnf-index']) or str(
                                                                    item['vnfd-id-ref']) != str(args['vnfd-id-ref'])]
            elif node_type == 'ns_cp':
                for vld in nsd['vld']:
                    if vld['id'] == args['vld_id']:
                        vld['vnfd-connection-point-ref'] = [item for item in vld['vnfd-connection-point-ref'] if
                                                            str(item['member-vnf-index-ref']) != str(
                                                                args['member-vnf-index-ref']) or str(
                                                                item['vnfd-id-ref']) != str(args['vnfd-id-ref'])]
        elif descriptor_type == 'vnfd':
            if 'vnfd-catalog' in descriptor:
                vnfd = descriptor['vnfd-catalog']['vnfd'][0]
            elif 'vnfd:vnfd-catalog' in descriptor:
                vnfd = descriptor['vnfd:vnfd-catalog']['vnfd'][0]

            if node_type == 'vnf_vl':
                vnfd['internal-vld'] = [item for item in vnfd['internal-vld'] if item['id'] != element_id]
            if node_type == 'cp':
                vnfd['connection-point'] = [item for item in vnfd['connection-point'] if item['name'] != args['name']]
                if vnfd['mgmt-interface']['cp'] == args['name']:
                    del vnfd['mgmt-interface']['cp']
                for vdu in vnfd['vdu']:
                    if 'interface' in vdu:
                        vdu['interface'] = [item for item in vdu['interface'] if 'external-connection-point-ref' not in item
                        or ('external-connection-point-ref'in item and item['external-connection-point-ref'] != args['name'])]
            if node_type == 'vdu':
                vdus = []
                for vdu in vnfd['vdu']:
                    if vdu['name'] != element_id:
                        vdus.append(vdu)
                    else:
                        for intcp in vdu['internal-connection-point']:
                            for intVld in vnfd['internal-vld']:
                                intVld['internal-connection-point'] = [item for item in intVld['internal-connection-point']
                                                                    if item['id-ref'] != intcp['id']]
                vnfd['vdu'] = vdus
            if node_type == 'int_cp':
                OsmUtil.remove_int_cp(element_id, vnfd)
        return descriptor

    @staticmethod
    def update_node(descriptor_type, descriptor, node_type, old, updated):
        if descriptor_type == 'nsd':
            if 'nsd-catalog' in descriptor:
                nsd = descriptor['nsd-catalog']['nsd'][0]
            elif 'nsd:nsd-catalog' in descriptor:
                nsd = descriptor['nsd:nsd-catalog']['nsd'][0]

            if node_type == 'ns_vl':
                for k, v in enumerate(nsd['vld']):
                    if v['id'] == old['id']:
                        nsd['vld'][k].update(updated)
            elif node_type == 'vnf':
                for k, v in enumerate(nsd['constituent-vnfd']):
                    if str(v['member-vnf-index']) == str(old['member-vnf-index']) and str(v['vnfd-id-ref']) == str(
                            old['vnfd-id-ref']):
                        print 'update here'
        elif descriptor_type == 'vnfd':
            if 'vnfd-catalog' in descriptor:
                vnfd = descriptor['vnfd-catalog']['vnfd'][0]
            elif 'vnfd:vnfd-catalog' in descriptor:
                vnfd = descriptor['vnfd:vnfd-catalog']['vnfd'][0]

            if node_type == 'vnf_vl':
                for k, v in enumerate(vnfd['internal-vld']):
                    if v['id'] == old['id']:
                        vnfd['internal-vld'][k].update(updated)
            if node_type == 'cp':
                for k, v in enumerate(vnfd['connection-point']):
                    if v['name'] == old['name']:
                        vnfd['connection-point'][k].update(updated)
                for vdu in vnfd['vdu']:
                    if 'interface' in vdu:
                        for intf in vdu['interface']:
                            if 'external-connection-point-ref' in intf and intf['external-connection-point-ref'] == old['name']:
                                intf['external-connection-point-ref'] = updated['name']
            if node_type == 'vdu':
                for k, v in enumerate(vnfd['vdu']):
                    if v['name'] == old['name']:
                        vnfd['vdu'][k].update(updated)

        return descriptor

    @staticmethod
    def add_base_node(descriptor_type, descriptor, node_type, element_id, args):
        if descriptor_type == 'nsd':
            if 'nsd-catalog' in descriptor:
                nsd = descriptor['nsd-catalog']['nsd'][0]
            elif 'nsd:nsd-catalog' in descriptor:
                nsd = descriptor['nsd:nsd-catalog']['nsd'][0]
            if node_type == 'ns_vl':
                nsd['vld'].append({
                    "vim-network-name": "PUBLIC",
                    "name": element_id,
                    "vnfd-connection-point-ref": [],
                    "mgmt-network": "true",
                    "type": "ELAN",
                    "id": element_id
                })
            if node_type == 'vnf':
                indexes = []
                for cvnfd in nsd['constituent-vnfd']:
                    indexes.append(int(cvnfd["member-vnf-index"]))
                memberindex = max(indexes) + 1 if len(indexes) > 0 else 1
                nsd['constituent-vnfd'].append({
                    "member-vnf-index": memberindex,
                    "vnfd-id-ref": element_id
                })
            if node_type == 'cp':
                for vld in nsd['vld']:
                    if vld['id'] == args['vld_id']:
                        if 'vnfd-connection-point-ref' not in vld:
                            vld['vnfd-connection-point-ref'] = []
                        vld['vnfd-connection-point-ref'].append(
                            {
                                "vnfd-connection-point-ref": args['vnfd-connection-point-ref'],
                                "member-vnf-index-ref": args['member-vnf-index-ref'],
                                "vnfd-id-ref": args['vnfd-id-ref']
                            },
                        )

        elif descriptor_type == 'vnfd':
            if 'vnfd-catalog' in descriptor:
                vnfd = descriptor['vnfd-catalog']['vnfd'][0]
            elif 'vnfd:vnfd-catalog' in descriptor:
                vnfd = descriptor['vnfd:vnfd-catalog']['vnfd'][0]
            if node_type == 'vdu':
                if 'vdu' not in vnfd:
                    vnfd['vdu'] = []
                vnfd['vdu'].append({
                    "count": "1",
                    "description": "",
                    "monitoring-param": [],
                    "internal-connection-point": [],
                    "image": "ubuntu",
                    "cloud-init-file": "",
                    "vm-flavor": {},
                    "interface": [],
                    "id": element_id,
                    "name": element_id
                })
            if node_type == 'cp':
                if 'connection-point' not in vnfd:
                    vnfd['connection-point'] = []
                vnfd['connection-point'].append({
                    "type": "VPORT",
                    "name": element_id
                })

            if node_type == 'vnf_vl':
                if 'internal-vld' not in vnfd:
                    vnfd['internal-vld'] = []
                vnfd['internal-vld'].append({
                    "short-name": element_id,
                    "name": element_id,
                    "internal-connection-point": [],
                    "type": "ELAN",
                    "ip-profile-ref": "",
                    "id": element_id
                })
            if node_type == 'interface':
                for vdu in vnfd['vdu']:
                    if vdu['id'] == args['vdu_id']:
                        vdu['interface'].append({
                            "virtual-interface": {
                                "type": "VIRTIO"
                            },
                            "name": args["name"],
                            "mgmt-interface": True,
                            "type": "EXTERNAL",
                            "external-connection-point-ref": args["external-connection-point-ref"]
                        })
            if node_type == 'int_cp':
                for vdu in vnfd['vdu']:
                    if vdu['id'] == args['vdu_id']:
                        if 'internal-connection-point' not in vdu:
                            vdu['internal-connection-point'] = []
                        vdu['internal-connection-point'].append({
                            "short-name": element_id,
                            "type": "VPORT",
                            "id": element_id,
                            "name": element_id
                        })
                        if 'interface' not in vdu:
                            vdu['interface'] = []
                        vdu['interface'].append({
                            "virtual-interface": {
                                "type": "VIRTIO"
                            },
                            "name": "int_"+element_id,
                            "type": "INTERNAL",
                            "internal-connection-point-ref": element_id
                        })
                for int_vld in vnfd['internal-vld']:
                    if int_vld['id'] == args['vld_id']:
                        if 'internal-connection-point' not in int_vld:
                            int_vld['internal-connection-point'] = []
                        int_vld['internal-connection-point'].append({
                            'id-ref': element_id
                        })
        return descriptor

    @staticmethod
    def update_graph_params(descriptor_type, descriptor, updated):
        if descriptor_type == 'nsd':
            if 'nsd-catalog' in descriptor:
                nsd = descriptor['nsd-catalog']['nsd'][0]
            elif 'nsd:nsd-catalog' in descriptor:
                nsd = descriptor['nsd:nsd-catalog']['nsd'][0]
            nsd.update(updated)
        elif descriptor_type == 'vnfd':
            if 'vnfd-catalog' in descriptor:
                vnfd = descriptor['vnfd-catalog']['vnfd'][0]
            elif 'vnfd:vnfd-catalog' in descriptor:
                vnfd = descriptor['vnfd:vnfd-catalog']['vnfd'][0]
            vnfd.update(updated)

        return descriptor

    @staticmethod
    def remove_int_cp(element_id, vnfd):
        for vdu in vnfd['vdu']:
            if 'interface' in vdu:
                vdu['interface'] = [item for item in vdu['interface'] if 'internal-connection-point-ref' not in item
                                    or ('internal-connection-point-ref' in item and item[
                    'internal-connection-point-ref'] != element_id)]
            if 'internal-connection-point' in vdu:
                vdu['internal-connection-point'] = [item for item in vdu['internal-connection-point'] if
                                                    item['id'] != element_id]
        for intVld in vnfd['internal-vld']:
            intVld['internal-connection-point'] = [item for item in intVld['internal-connection-point'] if
                                                   item['id-ref'] != element_id]

        return vnfd
