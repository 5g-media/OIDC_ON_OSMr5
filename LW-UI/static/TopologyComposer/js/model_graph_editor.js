/*
   Copyright 2017 CNIT - Consorzio Nazionale Interuniversitario per le Telecomunicazioni
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
if (typeof TCD3 === 'undefined') {
    var TCD3 = {};
}

TCD3.ModelGraphEditor = (function () {
    'use strict';

    var DEBUG = true;
    var SHIFT_BUTTON = 16;
    var IMAGE_PATH = "/static/assets/img/";


    ModelGraphEditor.prototype = new TCD3.GraphEditor();
    ModelGraphEditor.prototype.constructor = ModelGraphEditor;
    ModelGraphEditor.prototype.parent = TCD3.GraphEditor.prototype;

    /**
     * Constructor
     */
    function ModelGraphEditor(args) {

        log("Constructor");

    }


    ModelGraphEditor.prototype.init = function (args) {
        this.parent.init.call(this, args);
        var self = this;
        this.desc_id = args.desc_id || undefined; //TODO remove it

        this.type_property = {};
        this.type_property["unrecognized"] = args.gui_properties["nodes"]["default"];

        this._edit_mode = args.edit_mode || false;

        Object.keys(args.gui_properties["nodes"]).forEach(function (key, index) {

            this.type_property[key] = args.gui_properties["nodes"][key];

            this.type_property[key]["shape"] = this.parent.get_d3_symbol(this.type_property[key]["shape"]);
            if (this.type_property[key]["image"] !== undefined) {
                this.type_property[key]["image"] = IMAGE_PATH + this.type_property[key]["image"];
            }

        }, this);

        if (args.gui_properties["edges"]) {
            this.type_property_link = args.gui_properties["edges"];
            var link_types = ['unrecognized'].concat(Object.keys(self.type_property_link))
            this.defs.selectAll("marker")
                .data(link_types)
                .enter()
                .append("svg:marker")    // This section adds in the arrows
                .attr("id", function (d) {
                    return d;
                })
                .attr("viewBox", "-5 -5 10 10")
                .attr("refX", 13) /*must be smarter way to calculate shift*/
                .attr("refY", 0)
                .attr("markerUnits", "userSpaceOnUse")
                .attr("markerWidth", 12)
                .attr("markerHeight", 12)
                .attr("orient", "auto")
                .append("path")
                .attr("d", "M 0,0 m -5,-5 L 5,0 L -5,5 Z")
                .attr('fill', function (d) {
                    return self.type_property_link[d].color;
                });
        }

        this.customBehavioursOnEvents = args.behaviorsOnEvents || undefined;


        var data_url =  args.data_url || undefined;
        if (!args.graph_data && args.data_url) {
            d3.json(data_url, function (error, data) {
                //console.log(JSON.stringify(data))
                self.d3_graph.nodes = data.vertices;
                self.d3_graph.links = data.edges;
                self.d3_graph.graph_parameters = data.graph_parameters;
                self.model = data.model;
                self.refreshGraphParameters(self.d3_graph.graph_parameters);
                self.refresh();
                self.startForce();
                //if(args.filter_base != undefined)

                setTimeout(function () {
               self.handleForce(true);
                    self.handleFiltersParams(args.filter_base);
                }, 500);

            });
        } else {
            this.updateData(args)
        }
    }

    /**
     * Update data of the graph.
     * @param {Object} Required. An object that specifies tha data of the new node.
     * @returns {boolean}
     */
    ModelGraphEditor.prototype.updateData = function (args) {
        this.d3_graph.nodes = args.vertices;
        this.d3_graph.links = args.edges;
        this.d3_graph.graph_parameters = args.graph_parameters;
        this.model = args.model;
        this.refreshGraphParameters(this.d3_graph.graph_parameters);
        this.cleanAll();
        this.refresh();
        this.startForce();
        this.handleForce(this.forceSimulationActive);
        //this.force.restart();
        //if(args.filter_base != undefined)

        if(args.filter_base){
            var self = this;
            setTimeout(function () {
                self.handleForce(true);
                self.handleFiltersParams(args.filter_base);
            }, 500);
        }
    };

    /**
     * Add a new node to the graph.
     * @param {Object} Required. An object that specifies tha data of the new node.
     * @returns {boolean}
     */
    ModelGraphEditor.prototype.addNode = function (node, success, error) {
        var self = this;
        var current_layer = self.getCurrentView();
        var node_type = node.info.type;
        if (self.model.layer[current_layer] && self.model.layer[current_layer].nodes[node_type] && self.model.layer[current_layer].nodes[node_type].addable) {
            if (self.model.layer[current_layer].nodes[node_type].addable.callback) {
                console.log(self.model.callback)
                var c = self.model.callback[self.model.layer[current_layer].nodes[node_type].addable.callback].class;
                var controller = new TCD3.OsmController();
                controller[self.model.layer[current_layer].nodes[node_type].addable.callback](self, node, function (result) {
                    console.log(result)
                    console.log(node)
                    self.updateData(result);
                    // self.parent.addNode.call(self, node);
                    success && success();
                }, error);

            } else {

                log('addNode: callback undefined in model spec.');
                error && error("You can't add a " + node.info.type + ", callback undefined.");
            }
        } else {
            //FIXME Error handling????
            log("You can't add a " + node.info.type + " in a current layer " + current_layer);
            error && error("You can't add a " + node.info.type + " in a current layer " + current_layer);
        }
    };


    /**
     * Update the data properties of the node
     * @param {Object} Required. An object that specifies tha data of the node.
     * @returns {boolean}
     */
    ModelGraphEditor.prototype.updateDataNode = function (node, args, success, error) {
        console.log(node);
        var self = this;
        var controller = new  TCD3.OsmController();
        controller.updateNode(this,node, args, function(result){
            self.updateData(result);
            success && success();
        }, error);
    };

    /**
     * Update the data properties of the node
     * @param {Object} Required. An object that specifies tha data of the node.
     * @returns {boolean}
     */
    ModelGraphEditor.prototype.updateGraphParams = function (args, success, error) {
        var self = this;
        var controller = new  TCD3.OsmController();
        controller.updateGraphParams(args, function(result){
            self.updateData(result);
            success && success();
        }, error);
    };

    /**
     * Remove a node from graph and related links.
     * @param {String} Required. Id of node to remove.
     * @returns {boolean}
     */
    ModelGraphEditor.prototype.removeNode = function (node, success, error) {
        console.log('removeNode', JSON.stringify(node))
        var self = this;
        var current_layer = self.getCurrentView();
        var node_type = node.info.type;
        if (node.info.desc_id == undefined) {
            node.info.desc_id = self.desc_id;
        }
        if (self.model.layer[current_layer] && self.model.layer[current_layer].nodes[node_type] && self.model.layer[current_layer].nodes[node_type].removable) {
            if (self.model.layer[current_layer].nodes[node_type].removable.callback) {
                var c = self.model.callback[self.model.layer[current_layer].nodes[node_type].removable.callback].class;
                var controller = new  TCD3.OsmController();
                controller[self.model.layer[current_layer].nodes[node_type].removable.callback](self, node, function (result) {
                    self._deselectAllNodes();
                    self.updateData(result);
                    success && success();
                }, error);
            } else {

                log('removeNode: callback undefined in model spec.');
                error && error("You can't remove a " + node.info.type + ", callback undefined.");
            }
        } else {
            //FIXME we need to manage alert in a different way: FAILBACK
            log("You can't remove a " + node.info.type);
            error && error("You can't remove a " + node.info.type);
        }
    };

    /**
     * Add a new link to graph.
     * @param {Object} Required. An object that specifies tha data of the new Link.
     * @returns {boolean}
     */
    ModelGraphEditor.prototype.addLink = function (s, d, success, error) {
        var self = this;
        var source_id = s.id;
        var target_id = d.id;
        var source_type = s.info.type;
        var destination_type = d.info.type;
        var link = {
            source: s,
            target: d,
            view: this.filter_parameters.link.view[0],
            group: this.filter_parameters.link.group,
            desc_id: this.desc_id
        };
        log("addLink: " + JSON.stringify(link))
        var current_layer = self.getCurrentView()
        if (self.model.layer[current_layer].allowed_edges && self.model.layer[current_layer].allowed_edges[source_type] && self.model.layer[current_layer].allowed_edges[source_type].destination[destination_type]) {

            if (self.model.layer[current_layer].allowed_edges[source_type].destination[destination_type].callback) {
                var callback = self.model.layer[current_layer].allowed_edges[source_type].destination[destination_type].callback;
                console.log(callback, self.model.callback)
                var direct_edge = 'direct_edge' in self.model.layer[current_layer].allowed_edges[source_type].destination[destination_type] ? self.model.layer[current_layer].allowed_edges[source_type].destination[destination_type]['direct_edge'] : false;
                link.directed_edge = direct_edge;
                var c = self.model.callback[callback].class;
                var controller = new  TCD3.OsmController();
                controller[callback](self, link, function (result) {
                    self._deselectAllNodes();
                    self.updateData(result);
                    success && success();
                }, error);
            } else {
                log('addLink: callback undefined in model spec.');
                error && error("You can't add a link, callback undefined.");
            }

        } else {
            //FIXME we need to manage alert in a different way: FAILBACK
            log("You can't link a " + source_type + " with a " + destination_type);

            error && error("You can't link a " + source_type + " with a " + destination_type);
        }
    };

    /**
     * Remove a link from graph.
     * @param {String} Required. The identifier of link to remove.
     * @returns {boolean}
     */
    ModelGraphEditor.prototype.removeLink = function (link, success, error) {
        var self = this;
        var s = link.source;
        var d = link.target;
        var source_type = s.info.type;
        var destination_type = d.info.type;
        var current_layer = self.getCurrentView();
        console.log(self.model.layer[current_layer])
        if (self.model.layer[current_layer].allowed_edges && self.model.layer[current_layer].allowed_edges[source_type] && self.model.layer[current_layer].allowed_edges[source_type].destination[destination_type] &&
            self.model.layer[current_layer].allowed_edges[source_type].destination[destination_type].removable
        ) {
            if (self.model.layer[current_layer].allowed_edges[source_type].destination[destination_type].removable.callback) {
                var callback = self.model.layer[current_layer].allowed_edges[source_type].destination[destination_type].removable.callback;
                var c = self.model.callback[callback].class;
                var controller = new  TCD3.OsmController();
                controller[callback](self, link, function (result) {
                    self._deselectAllNodes();
                    self._deselectAllLinks();
                    
                    self.updateData(result);
                    // success && success();
                    success && success();
                }, error);
            } else {
                log('removeLink: callback undefined in model spec.');
                error && error("You can't remove a link, callback undefined.");
            }

        } else {
            //FIXME we need to manage alert in a different way: FAILBACK
            log("You can't delete the link");
            error && error("You can't delete the link");
        }


    };


    ModelGraphEditor.prototype.savePositions = function (data) {
        var vertices = {};
        this.node.each(function (d) {
            vertices[d.id] = {};
            vertices[d.id]['x'] = d.x;
            vertices[d.id]['y'] = d.y;
        });
        new TCD3.GraphRequests().savePositions({
            'vertices': vertices
        });

    };

    /**
     *  Internal functions
     */

    ModelGraphEditor.prototype._setupBehaviorsOnEvents = function (layer) {

        var self = this;
        var contextMenuLinksAction = [{
            title: 'Delete Link',
            action: function (elm, link, i) {
                self.removeLink(link, null, showAlert);
            },
            edit_mode: true
        }];
        var contextMenuNodesAction = [
            {
                title: 'Delete',
                action: function (elm, d, i) {
                    self.removeNode(d, null, showAlert);
                },
                edit_mode: true
            }

        ];
        if (this.customBehavioursOnEvents) {
            contextMenuNodesAction = contextMenuNodesAction.concat(this.customBehavioursOnEvents['behaviors'].nodes);
        }


        if (self.model && self.model.layer && self.model.layer[layer] && self.model.layer[layer].action && self.model.layer[layer].action.node) {
            for (var i in self.model.layer[layer].action.node) {
                var action = self.model.layer[layer].action.node[i]
                contextMenuNodesAction.push({
                    title: action.title,
                    action: function (elm, d, i) {
                        var callback = action.callback;
                        var c = self.model.callback[callback].class;
                        var controller = new TCD3[c]();
                        var args = {
                            elm: elm,
                            d: d,
                            i: i
                        };

                        controller[callback](self, args);
                    },
                    edit_mode: (action.edit_mode !== undefined) ? action.edit_mode : undefined
                });
            }
        }

        this.behavioursOnEvents = {
            'nodes': {
                'click': function (d) {

                    d3.event.preventDefault();

                    if (self._edit_mode && self.lastKeyDown === SHIFT_BUTTON && self._selected_node !== undefined) {
                        self.addLink(self._selected_node, d, null, showAlert);
                    } else {
                        self._selectNodeExclusive(this, d);
                    }

                },
                'mouseover': function (d) {
                    self.link.style('stroke-width', function (l) {
                        if (d === l.source || d === l.target)
                            return 4;
                        else
                            return 2;
                    });
                },
                'mouseout': function (d) {
                    self.link.style('stroke-width', 2);
                },
                'contextmenu': d3.contextMenu(contextMenuNodesAction, {
                    'edit_mode': self._edit_mode,
                    'layer': layer,
                    'type_object': 'node'
                })
            },
            'links': {
                'click': function (d) {
                    self._selectLinkExclusive(this, d);
                },
                'dblclick': function (event) {

                },
                'mouseover': function (d) {
                    d3.select(this).style('stroke-width', 4);
                },
                'mouseout': function (d) {
                    if (d !== self._selected_link)
                        d3.select(this).style('stroke-width', 2);
                },
                'contextmenu': d3.contextMenu(contextMenuLinksAction, {
                    'edit_mode': self._edit_mode,
                    'layer': layer,
                    'type_object': 'link'
                })
            }
        }
    };

    ModelGraphEditor.prototype.handleFiltersParams = function (filtersParams, notFireEvent) {

        this.parent.handleFiltersParams.call(this, filtersParams, notFireEvent);
        if (filtersParams && filtersParams.link && filtersParams.link.view)
            this._setupBehaviorsOnEvents(filtersParams.link.view[0]);
    };

    ModelGraphEditor.prototype.getAvailableNodes = function () {
        log('getAvailableNodes');
        log(this.model);
        if (this.model && this.model.layer[this.getCurrentView()] !== undefined)
            return this.model.layer[this.getCurrentView()].nodes;
        return [];
    };


    ModelGraphEditor.prototype.getTypeProperty = function () {
        return this.type_property;
    };

    ModelGraphEditor.prototype.getCurrentGroup = function () {
        return this.filter_parameters.node.group[0];
    };

    ModelGraphEditor.prototype.getCurrentView = function () {
        return this.filter_parameters.link.view[0];
    };
    ModelGraphEditor.prototype.getCurrentFilters = function () {
        return this.filter_parameters;
    };

    ModelGraphEditor.prototype.getGraphParams = function () {
        return this.d3_graph.graph_parameters;
    };

    /**
     * Log utility
     */
    function log(text) {
        if (DEBUG)
            console.log("::ModelGraphEditor::", text);
    }


    return ModelGraphEditor;


}(this));

if (typeof module === 'object') {
    module.exports = TCD3.ModelGraphEditor;
}
