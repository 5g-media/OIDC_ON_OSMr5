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

function performAction(instance_name, instance_id) {
    var url = '/instances/ns/'+instance_id+'/action';
    $("#formActionNS").attr("action", url);
    $('#modal_instance_new_action').modal('show');
}

function exportMetricNs(instance_name, instance_id) {
    var url = '/instances/ns/'+instance_id+'/monitoring/metric';
    $("#formExportMetricNS").attr("action", url);
    $('#modal_instance_export_metric').modal('show');
}

function newAlarmNs(instance_name, instance_id) {
    var url = '/instances/ns/'+instance_id+'/monitoring/alarm';
    $("#formAlarmNS").attr("action", url);
    $('#modal_instance_new_alarm').modal('show');
}

function deleteNs(instance_name, instance_id, force) {
    var url = '/instances/ns/'+instance_id+'/delete';
    bootbox.confirm("Are you sure want to delete " + instance_name + "?", function (result) {
        if (result) {
            if (force)
                url = url + '?force=true';
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
                error: function (result) {
                    dialog.modal('hide');
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
    })
}
function deleteNsi(instance_name, instance_id, force) {
    var url = '/instances/nsi/'+instance_id+'/delete';
    bootbox.confirm("Are you sure want to delete " + instance_name + "?", function (result) {
        if (result) {
            if (force)
                url = url + '?force=true';
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
                    console.log(result)
                    if (result['error'] == true){
                        dialog.modal('hide');
                        var data = result.responseJSON;
                        var title = "Error " + (data && data.code ? data.code : 'unknown');
                        var message = data && data.detail ? data.detail : 'No detail available.';
                        bootbox.alert({
                            title: title,
                            message: message
                        });
                    }
                    else {
                        dialog.modal('hide');
                        location.reload();
                    }
                },
                error: function (result) {
                    dialog.modal('hide');
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
    })
}

function deletePDU(instance_name, instance_id) {
    var url = '/instances/pdu/'+instance_id+'/delete';
    bootbox.confirm("Are you sure want to delete " + instance_name + "?", function (result) {
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

var addFormGroup = function (event) {
    event.preventDefault();

    var $formGroup = $(this).closest('.form-group');
    var $formGroupClone = $formGroup.clone();

    $(this)
        .toggleClass('btn-success btn-add btn-danger btn-remove')
        .html('–');

    $formGroupClone.find('input').val('');
    $formGroupClone.insertAfter($formGroup);

};

var removeFormGroup = function (event) {
    event.preventDefault();
    var $formGroup = $(this).closest('.form-group');
    $formGroup.remove();
};

var addInterfaceGroup = function (event) {
    event.preventDefault();

    var $formGroup = $(this).closest('.interface-group');
    var $formGroupClone = $formGroup.clone();

    $(this)
        .toggleClass('btn-success btn-add btn-danger btn-remove')
        .html('–');

    $formGroupClone.find('input').val('');
    $formGroupClone.insertAfter($formGroup);

};

var removeInterfaceGroup = function (event) {
    event.preventDefault();
    var $formGroup = $(this).closest('.interface-group');
    $formGroup.remove();
};

function showTopology(type, instance_id) {
    var url = '/instances/'+type+'/'+instance_id+'/topology';
    window.location = url;
}

function showInstanceDetails(type, instance_id) {
    var url_info = '/instances/'+type+'/'+instance_id;
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

            if (result['data'] !== undefined) {
                editorJSON.setValue(JSON.stringify(result['data'], null, "\t"));
                editorJSON.setOption("autoRefresh", true);
                dialog.modal('hide');
                $('#modal_show_instance').modal('show');
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

var editorJSON;

$(document).ready(function () {
    var json_editor_settings = {
        mode: "javascript",
        showCursorWhenSelecting: true,
        autofocus: true,
        lineNumbers: true,
        lineWrapping: true,
        foldGutter: true,
        gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
        autoCloseBrackets: true,
        matchBrackets: true,
        extraKeys: {
            "F11": function (cm) {
                cm.setOption("fullScreen", !cm.getOption("fullScreen"));
            },
            "Esc": function (cm) {
                if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);
            },
            "Ctrl-Q": function (cm) {
                cm.foldCode(cm.getCursor());
            }
        },
        theme: "neat",
        keyMap: "sublime"
    };
    var myJsonTextArea = document.getElementById("instance_view_json");
    editorJSON = CodeMirror(function (elt) {
        myJsonTextArea.parentNode.replaceChild(elt, myJsonTextArea);
    }, json_editor_settings);


    $(document).on('click', '.primitive-group .btn-add', addFormGroup);
    $(document).on('click', '.primitive-group .btn-remove', removeFormGroup);

    $(document).on('click', '.interface-group .btn-add', addInterfaceGroup);
    $(document).on('click', '.interface-group .btn-remove', removeInterfaceGroup);

    $("#formCreatePDU").submit(function (event) {
        event.preventDefault(); //prevent default action
        var post_url = $(this).attr("action"); //get form action url
        var request_method = $(this).attr("method"); //get form GET/POST method
        var form_data = new FormData(this); //Encode form elements for submission
        $.ajax({
            url: post_url,
            type: request_method,
            data: form_data,
            headers: {
                "Accept": 'application/json'
            },
            contentType: false,
            processData: false
        }).done(function (response, textStatus, jqXHR) {
            table.ajax.reload();
            $('#modal_new_pdu').modal('hide');
        }).fail(function (result) {
            var data = result.responseJSON;
            var title = "Error " + (data.code ? data.code : 'unknown');
            var message = data.detail ? data.detail : 'No detail available.';
            bootbox.alert({
                title: title,
                message: message
            });
        });
    });

    $("#formActionNS").submit(function (event) {
        event.preventDefault(); //prevent default action
        var post_url = $(this).attr("action"); //get form action url
        var request_method = $(this).attr("method"); //get form GET/POST method
        var form_data = new FormData(this); //Encode form elements for submission
        console.log(post_url);
        $.ajax({
            url: post_url,
            type: request_method,
            data: form_data,
            headers: {
                "Accept": 'application/json'
            },
            contentType: false,
            processData: false
        }).done(function (response, textStatus, jqXHR) {
            $('#modal_instance_new_action').modal('hide');
            bootbox.alert({
                title: "Action",
                message: "Action received."
            });
        }).fail(function (result) {
            var data = result.responseJSON;
            var title = "Error " + (data.code ? data.code : 'unknown');
            var message = data.detail ? data.detail : 'No detail available.';
            bootbox.alert({
                title: title,
                message: message
            });
        });
    });

    $("#formAlarmNS").submit(function (event) {
        event.preventDefault(); //prevent default action
        var post_url = $(this).attr("action"); //get form action url
        var request_method = $(this).attr("method"); //get form GET/POST method
        var form_data = new FormData(this); //Encode form elements for submission
        console.log(post_url);
        $.ajax({
            url: post_url,
            type: request_method,
            data: form_data,
            headers: {
                "Accept": 'application/json'
            },
            contentType: false,
            processData: false
        }).done(function (response, textStatus, jqXHR) {
            $('#modal_instance_new_action').modal('hide');
            bootbox.alert({
                title: "Metric",
                message: "Alarm created."
            });
        }).fail(function (result) {
            var data = result.responseJSON;
            var title = "Error " + (data.code ? data.code : 'unknown');
            var message = data.detail ? data.detail : 'No detail available.';
            bootbox.alert({
                title: title,
                message: message
            });
        });
    });

    $("#formExportMetricNS").submit(function (event) {
        event.preventDefault(); //prevent default action
        var post_url = $(this).attr("action"); //get form action url
        var request_method = $(this).attr("method"); //get form GET/POST method
        var form_data = new FormData(this); //Encode form elements for submission
        console.log(post_url);
        $.ajax({
            url: post_url,
            type: request_method,
            data: form_data,
            headers: {
                "Accept": 'application/json'
            },
            contentType: false,
            processData: false
        }).done(function (response, textStatus, jqXHR) {
            $('#modal_instance_new_action').modal('hide');
            bootbox.alert({
                title: "Metric",
                message: "Metric exported."
            });
        }).fail(function (result) {
            var data = result.responseJSON;
            var title = "Error " + (data.code ? data.code : 'unknown');
            var message = data.detail ? data.detail : 'No detail available.';
            bootbox.alert({
                title: title,
                message: message
            });
        });
    });

});