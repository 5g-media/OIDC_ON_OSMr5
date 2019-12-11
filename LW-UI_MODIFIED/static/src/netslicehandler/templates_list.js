/*
   Copyright 2019 EveryUP Srl

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

function deleteTemplate(template_name, template_id) {
    var url = '/netslices/templates/'+template_id+'/delete';
    bootbox.confirm("Are you sure want to delete " + template_name + "?", function (result) {
        if (result) {
            var dialog = bootbox.dialog({
                message: '<div class="text-center"><i class="fa fa-spin fa-spinner"></i> Loading...</div>',
                closeButton: true
            });
            $.ajax({
                url: url,
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

function showNstDetails(template_id) {
    var url_info = '/netslices/templates/'+template_id+'/details';
    var dialog = bootbox.dialog({
        message: '<div class="text-center"><i class="fa fa-spin fa-spinner"></i> Loading...</div>',
        closeButton: true
    });
    $.ajax({
        url: url_info,
        type: 'GET',
        dataType: "json",
        contentType: "application/json;charset=utf-8",
        success: function (result) {
            console.log(result)
            if (result['data'] !== undefined) {
                editorJSON.setValue(JSON.stringify(result['data'], null, "\t"));
                editorJSON.setOption("autoRefresh", true);
                dialog.modal('hide');
                $('#modal_show_nst').modal('show');
            }
            else {
                dialog.modal('hide');
                bootbox.alert("An error occurred while retrieving the information.");
            }
        },
        error: function (result) {
            dialog.modal('hide');
            bootbox.alert("An error occurred while retrieving the information.");
        }
    });
}