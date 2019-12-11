/*
   Copyright 2018 CNIT - Consorzio Nazionale Interuniversitario per le Telecomunicazioni

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

function openModalCreatePDU(args) {
    var select2_groups = $('#pdu_vim_accounts').select2({
        placeholder: 'Select Vims',
        width: '100%',
        ajax: {
            url: args.vim_list_url,
            dataType: 'json',
            processResults: function (data) {
                vims = [];
                if (data['datacenters']) {
                    for (d in data['datacenters']) {
                        var datacenter = data['datacenters'][d];
                        vims.push({ id: datacenter['_id'], text: datacenter['name'] })
                    }
                }
                return {
                    results: vims
                };
            }
        }
    });

    $('#modal_new_pdu').modal('show');
}

function openModalCreateNS(args) {
    // load vim account list
    select2_groups = $('#vimAccountId').select2({
        placeholder: 'Select VIM',
        width: '100%',
        ajax: {
            url: args.vim_list_url,
            dataType: 'json',
            processResults: function (data) {
                vims = [];
                if (data['datacenters']) {
                    for (d in data['datacenters']) {
                        var datacenter = data['datacenters'][d];
                        vims.push({ id: datacenter['_id'], text: datacenter['name'] })
                    }
                }

                return {
                    results: vims
                };
            }
        }
    });

    // load nsd list
    select2_groups = $('#nsdId').select2({
        placeholder: 'Select NSD',
        width: '100%',
        ajax: {
            url: args.nsd_list_url,
            dataType: 'json',
            processResults: function (data) {
                nsd_list = [];

                if (data['descriptors']) {
                    for (d in data['descriptors']) {
                        var nsd = data['descriptors'][d];
                        nsd_list.push({ id: nsd['_id'], text: nsd['name'] })
                    }
                }

                return {
                    results: nsd_list
                };
            }
        }
    });

    if (args.descriptor_id) {
        // Set the value, creating a new option if necessary
        if ($('#nsdId').find("option[value='" + args.descriptor_id + "']").length) {
            $('#nsdId').val(args.descriptor_id).trigger('change');
        } else {
            // Create a DOM Option and pre-select by default
            var newOption = new Option(args.descriptor_name, args.descriptor_id, true, true);
            // Append it to the select
            $('#nsdId').append(newOption).trigger('change');
        }
    }

    $('#modal_new_instance').modal('show');
}
function openModalCreateNSI(args) {
    // load vim account list
    select2_groups = $('#vimAccountIdNSI').select2({
        placeholder: 'Select VIM',
        width: '100%',
        ajax: {
            url: args.vim_list_url,
            dataType: 'json',
            processResults: function (data) {
                vims = [];
                if (data['datacenters']) {
                    for (d in data['datacenters']) {
                        var datacenter = data['datacenters'][d];
                        vims.push({ id: datacenter['_id'], text: datacenter['name'] })
                    }
                }

                return {
                    results: vims
                };
            }
        }
    });

    // load nsd list
    select2_groups = $('#nstId').select2({
        placeholder: 'Select NST',
        width: '100%',
        ajax: {
            url: args.nst_list_url,
            dataType: 'json',
            processResults: function (data) {
                nst_list = [];

                if (data['templates']) {
                    for (d in data['templates']) {
                        var nst = data['templates'][d];
                        nst_list.push({ id: nst['_id'], text: nst['name'] })
                    }
                }

                return {
                    results: nst_list
                };
            }
        }
    });
    if (args.template_id) {
        // Set the value, creating a new option if necessary
        if ($('#nstId').find("option[value='" + args.template_id + "']").length) {
            $('#nstId').val(args.template_id).trigger('change');
        } else {
            // Create a DOM Option and pre-select by default
            var newOption = new Option(args.template_name, args.template_id, true, true);
            // Append it to the select
            $('#nstId').append(newOption).trigger('change');
        }
    }

    $('#modal_new_nsi').modal('show');
}