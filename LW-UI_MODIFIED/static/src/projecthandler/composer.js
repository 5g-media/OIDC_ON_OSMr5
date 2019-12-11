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
var graph_editor = new dreamer.ModelGraphEditor();
var selected_vnffgId = null;
var show_all = null;

// Enable Drop Action on the Graph
initDropOnGraph();

var type_view = {
    "ns": ["vnf", "ns_vl"],
    "vnf": ["vdu", "cp"]
};

var params = {
        node: {
            type: type_view['ns'],
            group: []
        },
        link: {
            group: [],
            view: ['ns']
        }
    };
$(document).ready(function() {

    graph_editor.addListener("filters_changed", changeFilter);
    graph_editor.addListener("refresh_graph_parameters", refreshGraphParameters);

    console.log(osm_gui_properties)
    // graph_editor initialization
    graph_editor.init({
        width: $('#graph_ed_container').width(),
        height: $('#graph_ed_container').height(),
        data_url: window.location.href,
        desc_id: getUrlParameter('id'),
        gui_properties: osm_gui_properties,
        behaviorsOnEvents:{
            viewBased: false,
            behaviors: buildBehaviorsOnEvents()
        }
    });
    // this will filter in the different views, excluding the node types that are not listed in params
    graph_editor.handleFiltersParams(params);

});

var filters = function(e, params) {
    graph_editor.handleFiltersParams(params);
    $('#' + e).nextAll('li').remove();
}


function initDropOnGraph() {

    var dropZone = document.getElementById('graph_ed_container');
    dropZone.ondrop = function(e) {
        var group = graph_editor.getCurrentGroup()
        e.preventDefault();
        var elemet_id = e.dataTransfer.getData("text/plain");
        var nodetype = $('#'+elemet_id).attr('type-name');
        console.log(nodetype);
        if (nodetype) {
            var type_name = graph_editor.getTypeProperty()[nodetype].name;
                $('#div_chose_id').show();
                $('#input_choose_node_id').val(nodetype + "_" + generateUID());
                $('#modal_chooser_title_add_node').text('Add ' + type_name);
                $('#save_choose_node_id').off('click').on('click', function() {
                    var name = $('#input_choose_node_id').val();
                    var node_information = {
                        'id': name,
                        'info': {
                            'type': nodetype,
                            'group': [group],
                            'desc_id': getUrlParameter('id'),
                        },
                        'x': e.layerX,
                        'y': e.layerY
                    }
                    console.log(JSON.stringify(node_information))
                    graph_editor.addNode(node_information, function() {
                        $('#modal_choose_node_id').modal('hide');
                    }, function(error){
                        showAlert(error)
                    });
                });
                $('#modal_choose_node_id').modal('show');


        }

    }

    dropZone.ondragover = function(ev) {
        console.log("ondragover");
        return false;
    }

    dropZone.ondragleave = function() {
        console.log("ondragleave");
        return false;
    }
}

function handleForce(el) {
    if (el.id == "topology_play") {
        $("#topology_pause").removeClass('active');
        $("#topology_play").addClass('active');
    } else {
        $("#topology_pause").addClass('active');
        $("#topology_play").removeClass('active');
    }

    graph_editor.handleForce((el.id == "topology_play") ? true : false);

}

function changeFilter(e, c) {

    console.log("changeFilter", JSON.stringify(c));
    //$("#title_header").text("OSHI Graph Editor");
    //updateNodeDraggable({type_property: type_property, nodes_layer: graph_editor.getAvailableNodes()})
    if(c)
        new dreamer.GraphRequests().getAvailableNodes({layer: c.link.view[0]}, buildPalette, showAlert);

}

function refreshGraphParameters(e, graphParameters) {
    var self = $(this);
    if (graphParameters == null) return;

}

function resetFilters(){
    graph_editor.handleFiltersParams(params);
}

function buildBehaviorsOnEvents() {
    var self = this;
    var contextmenuNodesAction = [{
        title: 'Show info',
        action: function (elm, d, i) {
           // console.log('Show NodeInfo', elm, d, i);
            var nodeData = {
                "node": {
                    "id": d.id
                }
            };
        },
        edit_mode: false

    },
        {
            title: 'Explore',
            action: function (elm, c_node, i) {
                if (c_node.info.type != undefined) {
                    var current_layer_nodes = Object.keys(graph_editor.model.layer[graph_editor.getCurrentView()].nodes);
                    if (current_layer_nodes.indexOf(c_node.info.type) >= 0) {
                        if (graph_editor.model.layer[graph_editor.getCurrentView()].nodes[c_node.info.type].expands) {
                            var new_layer = graph_editor.model.layer[graph_editor.getCurrentView()].nodes[c_node.info.type].expands;
                            graph_editor.handleFiltersParams({
                                node: {
                                    type: Object.keys(graph_editor.model.layer[new_layer].nodes),
                                    group: [c_node.id]
                                },
                                link: {
                                    group: [c_node.id],
                                    view: [new_layer]
                                }
                            });

                        }
                        else {
                            showAlert('This is not an explorable node.')
                        }
                    }
                }
            },
            edit_mode: false
        }];
    var behavioursOnEvents = {
        'nodes': contextmenuNodesAction

    };

    return behavioursOnEvents;
}