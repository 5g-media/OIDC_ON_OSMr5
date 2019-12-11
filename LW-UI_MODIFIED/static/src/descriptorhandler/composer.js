/*
   Copyright 2018 EveryUP srl

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an  BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

//GraphEditor instance
var graph_editor = new TCD3.ModelGraphEditor();

var type_view = {
    "nsd": ["vnf", "ns_vl", "ns_cp"],
    "vnfd": ["vdu", "cp", "vnf_vl", "int_cp"]
};

var map = {
    'ip-address': 'IP', 'vnfd-id': 'Vnfd Id', 'vnfd-ref': 'Vnfd Ref', 'vim-account-id': 'Vim Id',
    'member-vnf-index-ref': 'Member index', 'created-time': 'Created', 'id': 'Id', 'mgmt-network': 'Mgmt network',
    'name': 'Name', 'type': 'Type', 'vim-network-name': 'Vim network name', 'connection-point-id': 'Cp Id',
    'vdu-id-ref': 'Vdu Id', 'nsr-id-ref': 'Nsr Id'
};

var params = {
    node: {
        type: type_view[getUrlParameter('type')],
        group: []
    },
    link: {
        group: [],
        view: [getUrlParameter('type')]
    }
};

$(document).ready(function () {

    graph_editor.addListener("filters_changed", changeFilter);
    graph_editor.addListener("node:selected", refreshElementInfo);
    graph_editor.addListener("node:deselected", refreshElementInfo);

    // graph_editor initialization
    graph_editor.init({
        width: $('#graph_editor_container').width(),
        height: $('#graph_editor_container').height(),

        data_url: window.location.href,
        //desc_id: getUrlParameter('id'),
        gui_properties: osm_gui_properties,
        edit_mode: true,
        behaviorsOnEvents: {
            viewBased: false,
            behaviors: buildBehaviorsOnEvents()
        }
    });
    graph_editor.handleFiltersParams(params);
    initDropOnGraph();


    $("#side_form").submit(function (event) {
        event.preventDefault(); //prevent default action
        console.log("ON submit")
        var form_data = new FormData(this); //Encode form elements for submission
        var formDataJson = {};
        form_data.forEach(function (value, key) {
            formDataJson[key] = value;
        });
        var dialog = bootbox.dialog({
            message: '<div class="text-center"><i class="fa fa-spin fa-spinner"></i> Updating...</div>',
            closeButton: true
        });
        if (graph_editor._selected_node) {
            graph_editor.updateDataNode(graph_editor._selected_node, formDataJson, function () {
                dialog.modal('hide');
            }, function (result) {
                var data = result.responseJSON;
                var title = "Error " + (data && data.code ? data.code : 'unknown');
                var message = data && data.detail ? data.detail : 'No detail available.';
                dialog.modal('hide');
                bootbox.alert({
                    title: title,
                    message: message
                });
            })
        } else {
            graph_editor.updateGraphParams(formDataJson, function () {
                dialog.modal('hide');
            }, function (result) {
                var data = result.responseJSON;
                var title = "Error " + (data && data.code ? data.code : 'unknown');
                var message = data && data.detail ? data.detail : 'No detail available.';
                dialog.modal('hide');
                bootbox.alert({
                    title: title,
                    message: message
                });
            })
        }

    });
});


function initDropOnGraph() {

    var dropZone = document.getElementById('graph_editor_container');
    dropZone.ondrop = function (e) {
        var group = graph_editor.getCurrentGroup();
        e.preventDefault();
        var elemet_id = e.dataTransfer.getData("text/plain");

        var nodetype = $('#' + elemet_id).attr('type-name');
        var random_name = nodetype + "_" + generateUID();
        console.log(nodetype)
        var node_information = {
            'id': random_name,
            'info': {
                'type': nodetype,
                'property': {
                    'custom_label': random_name
                },
                'group': null,
                'desc_id': getUrlParameter('id'),
                'desc_type': getUrlParameter('type'),
                'osm': {}
            },
            'x': e.layerX,
            'y': e.layerY
        };

        if (nodetype === 'vnf') {
            node_information['id'] = $('#' + elemet_id).attr('desc_id');
        }

        graph_editor.addNode(node_information, function () {
            console.log("OK")
        }, function (result) {
            var data = result.responseJSON;
            var title = "Error " + (data && data.code ? data.code : 'unknown');
                var message = data && data.detail ? data.detail : 'No detail available.';
                bootbox.alert({
                    title: title,
                    message: message
                });
        })

    };

    dropZone.ondragover = function (ev) {
        console.log("ondragover");
        return false;
    };

    dropZone.ondragleave = function () {
        console.log("ondragleave");
        return false;
    };
}


function handleForce(el) {
    graph_editor.handleForce((el.getAttribute('aria-pressed') === "true"));
}

function changeFilter(e, c) {
    if (c && c.link && c.link.view[0]) {
        updateLegend(c.link.view[0]);
        updatePalette(c.link.view[0]);
    }
    layerDetails(graph_editor.getCurrentFilters())
}

function resetFilters() {
    graph_editor.handleFiltersParams(params);
}

function buildBehaviorsOnEvents() {
    var contextmenuNodesAction = [];
    return {
        'nodes': contextmenuNodesAction
    };

}

function refreshElementInfo(event, element) {
    if (event.type === 'node:selected') {
        switch (element.info.type) {
            case 'vnf':
                vnfDetails(element.info.osm);
                break;
            case 'vdu':
                vduDetails(element.info.osm);
                break;
            case 'int_cp':
                intcpDetails(element.info.osm);
                break;
            case 'ns_cp':
                nscpDetails(element.info.osm);
                break;
            case 'cp':
                cpDetails(element.info.osm);
                break;
            case 'vnf_vl':
            case 'ns_vl':
                vlDetails(element.info.osm);
                break;
        }
    }
    else if (event.type === 'node:deselected') {
        layerDetails(graph_editor.getCurrentFilters())
    }
}

function layerDetails(filters) {
    var side = $('#side_form');
    var graph_parameters = graph_editor.getGraphParams();
    var layer_template = '';
    if (graph_parameters['view'] && filters.link.view.length > 0 && filters.link.view[0]) {
        if (filters.link.view[0] === 'nsd') {
            layer_template = getMainSectionWithSubmitButton('NSD');
            layer_template += getChildrenTable(graph_parameters['view']['nsd']);
        }
        else if (filters.link.view[0] === 'vnfd') {
            layer_template = getMainSectionWithSubmitButton('VNFD');

            layer_template += getChildrenTable(graph_parameters['view']['vnfd']);
        }
    }

    side.empty();
    side.append(layer_template)
}

function updateLegend(view) {
    var legend = $('#legenda');
    var nodes = type_view[view];
    var legend_template = '';
    var nodes_properties = osm_gui_properties['nodes'];
    for (var n in nodes) {
        var node = nodes[n];
        if (nodes_properties[node]) {
            legend_template += '<div class="node">' +
                '<div class="icon" style="background-color:' + nodes_properties[node].color + '"></div>' +
                '<div class="name">' + nodes_properties[node].name + '</div></div>';
        }
    }

    legend.empty();
    legend.append(legend_template)

}

function updatePalette(view) {
    var palette = $('#palette');
    var palette_template = '';
    palette.empty();
    if (view === 'vnfd') {
        var nodes = type_view[view];
        var nodes_properties = osm_gui_properties['nodes'];
        for (var n in nodes) {
            var node = nodes[n];
            if (nodes_properties[node]) {
                palette_template += '<div id="drag_' + n + '" class="node ui-draggable"' +
                    'type-name="' + node + '" draggable="true" ondragstart="nodeDragStart(event)">' +
                    '<div class="icon" style="background-color:' + nodes_properties[node].color + '"></div>' +
                    '<div class="name">' + nodes_properties[node].name + '</div></div>';
            }
        }

        palette.append(palette_template)
    } else if (view === 'nsd') {
        $.ajax({
            url: '/projects/descriptors/composer/availablenodes?layer=nsd',
            type: 'GET',
            cache: false,
            success: function (result) {
                palette_template += '<div id="drag_ns_vl" class="node ui-draggable"' +
                    'type-name="ns_vl" draggable="true" ondragstart="nodeDragStart(event)">' +
                    '<div class="icon" style="background-color:' + osm_gui_properties['nodes']['ns_vl'].color + '"></div>' +
                    '<div class="name">' + osm_gui_properties['nodes']['ns_vl'].name + '</div></div>';
                palette_template += getSubSection('VNFD');
                for (var d in result['descriptors']) {
                    var desc = result['descriptors'][d];
                    palette_template += '<div id="drag_' + desc.id + '" class="node ui-draggable"' +
                        'type-name="vnf" desc_id="' + desc.id + '" draggable="true" ondragstart="nodeDragStart(event)">' +
                        '<div class="icon" style="background-color:#605ca8"></div>' +
                        '<div class="name">' + desc.name + '</div></div>';
                }
                palette.append(palette_template)
            },
            error: function (result) {
                var data = result.responseJSON;
                var title = "Error " + (data && data.code ? data.code : 'unknown');
                var message = data && data.detail ? data.detail : 'No detail available.';
                bootbox.alert({
                    title: title,
                    message: message
                });
            }
        });
    }

}


function vnfDetails(vnfr) {
    var side = $('#side_form');
    var vnfr_template = getMainSection('VNF');

    vnfr_template += getChildrenTable(vnfr, true);
    side.empty();
    side.append(vnfr_template)
}

function vduDetails(vdur) {
    var side = $('#side_form');
    var vdur_template = getMainSectionWithSubmitButton('VDU');
    vdur_template += getChildrenTable(vdur);

    side.empty();
    side.append(vdur_template)
}

function intcpDetails(cp) {
    var side = $('#side_form');
    var cp_template = getMainSection('Int. Connection Point');

    cp_template += getChildrenTable(cp, true);
    side.empty();
    side.append(cp_template);
}

function cpDetails(cp) {
    var side = $('#side_form');
    var cp_template = getMainSectionWithSubmitButton('Connection Point');

    cp_template += getChildrenTable(cp);
    side.empty();
    side.append(cp_template);
}

function nscpDetails(cp) {
    var side = $('#side_form');
    var cp_template = getMainSection('Connection Point');

    cp_template += getChildrenTable(cp, true);
    side.empty();
    side.append(cp_template);
}

function vlDetails(vl) {
    var side = $('#side_form');
    var vl_template = getMainSectionWithSubmitButton('Virtual Link');

    vl_template += getChildrenTable(vl);
    side.empty();
    side.append(vl_template);
}


function getMainSection(title) {
    return '<div class="section"><span style="font-weight: 500;">' + title + '</span></div>';
}

function getMainSectionWithSubmitButton(title) {
    return '<div class="section"><span style="font-weight: 500;">' + title + '</span>' +
        '<div class="status"><button id="update_button" class="btn btn-xs btn-default" ><i class="fa fa-save"></i> SAVE</button></div></div>';
}

function getSubSection(title) {
    return '<div class="section"><span>' + title + '</span></div>';
}

function getMainSectionWithStatus(title, status) {
    var template = '<div class="section"><span style="font-weight: 500;">' + title + '</span>';
    if (status)
        template += '<div class="status active"><span class="indicator"></span> ACTIVE</div>';
    else
        template += '<div class="status"><span class="indicator"></span>NO ACTIVE</div>';
    template += '</div>';
    return template;
}

function getChildrenTable(data, ro) {
    var template = '<table class="children">';

    for (var key in data) {
        if (typeof data[key] !== 'object') {
            var key_map = (map[key]) ? map[key] : key;
            if (ro)
                template += '<tr><td>' + key_map + '</td><td>' + data[key] + '</td></tr>';
            else
                template += '<tr><td>' + key_map + '</td><td><input name="' + key + '" class="form-control input-sm" type="text"  value="' + data[key] + '"></td></tr>';

        }
    }
    template += '</table>';
    return template;
}

function openHelp() {
    $('#modalTopologyInfoButton').modal('show');
}

function openTextedit() {
    window.location.href = '/projects/descriptors/' + getUrlParameter('type') + '/' + getUrlParameter('id')
}