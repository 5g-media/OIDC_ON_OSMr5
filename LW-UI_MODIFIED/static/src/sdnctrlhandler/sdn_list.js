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

function deleteSDN(sdn_uuid, name) {
    bootbox.confirm("Are you sure want to delete " + name +"?", function (result) {
        if (result) {
            var dialog = bootbox.dialog({
                message: '<div class="text-center"><i class="fa fa-spin fa-spinner"></i> Loading...</div>',
                closeButton: true
            });
            $.ajax({
                url: '/sdn/' + sdn_uuid + '/delete',
                type: 'GET',
                dataType: "json",
                contentType: "application/json;charset=utf-8",
                success: function (result) {
                    if (result['error'] == true){
                        dialog.modal('hide');
                        bootbox.alert("An error occurred.");
                    }
                    else {
                        dialog.modal('hide');
                        location.reload();
                    }
                },
                error: function (error) {
                    dialog.modal('hide');
                    bootbox.alert("An error occurred.");
                }
            });
        }
    })
}

function showSDN(sdn_uuid) {
    var dialog = bootbox.dialog({
        message: '<div class="text-center"><i class="fa fa-spin fa-spinner"></i> Loading...</div>',
        closeButton: true
    });

    $.ajax({
        url: '/sdn/' + sdn_uuid ,
        type: 'GET',
        dataType: "json",
        contentType: "application/json;charset=utf-8",
        success: function (result) {
            //$('#modal_show_vim_body').empty();
            var sdn = result.sdn;
            if (sdn) {
                $('#modal_show_sdn_body').find('span').text('-');
                for (var k in sdn) {
                    $('#' + k).text(sdn[k])
                }
                if (sdn['_admin']) {
                    for (var i in sdn['_admin']) {
                        if (i === 'modified' || i === 'created') {
                            //$('#' + i).text(new Date(sdn['_admin'][i]* 1000).toUTCString());
                            $('#' + i).text(moment(sdn['_admin'][i] * 1000).format('DD/MM/YY hh:mm:ss'));
                        }
                        else if (i === 'deployed') {
                            $('#' + i).text(JSON.stringify(sdn['_admin'][i]))
                        }
                        else
                            $('#' + i).text(sdn['_admin'][i])
                    }
                }
                dialog.modal('hide');
                $('#modal_show_sdn').modal('show');
            }
            else {
                dialog.modal('hide');
                bootbox.alert("An error occurred while retrieving the SDN controller info.");
            }

        },
        error: function (result) {
            dialog.modal('hide');
            bootbox.alert("An error occurred while retrieving the SDN controller info.");
        }
    });

}