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

function deletePackage(package_type, package_id, package_name) {

    bootbox.confirm("Are you sure want to delete " + package_name + "?", function (result) {
        if (result) {
            var dialog = bootbox.dialog({
                message: '<div class="text-center"><i class="fa fa-spin fa-spinner"></i> Loading...</div>',
                closeButton: true
            });
            $.ajax({
                url: '/packages/' + package_type + '/' + package_id + '/delete',
                type: 'GET',
                dataType: "json",
                contentType: "application/json;charset=utf-8",
                success: function (result) {
                    dialog.modal('hide');
                    location.reload();
                },
                error: function (result) {
                    dialog.modal('hide');
                    bootbox.alert("An error occurred.");
                }
            });
        }
    })
}

function clonePackage(package_type, package_id) {

    bootbox.confirm("Are you sure want to clone?", function (result) {
        if (result) {
            var dialog = bootbox.dialog({
                message: '<div class="text-center"><i class="fa fa-spin fa-spinner"></i> Loading...</div>',
                closeButton: true
            });
            $.ajax({
                url: '/packages/' + package_type + '/' + package_id + '/clone',
                type: 'GET',
                dataType: "json",
                contentType: "application/json;charset=utf-8",
                success: function (result) {
                    dialog.modal('hide');
                    location.reload();
                },
                error: function (result) {
                    dialog.modal('hide');
                    bootbox.alert("An error occurred.");
                }
            });
        }
    })
}


function openPackageContentList(type, pkg_id) {
    var dialog = bootbox.dialog({
        message: '<div class="text-center"><i class="fa fa-spin fa-spinner"></i> Loading...</div>',
        closeButton: true
    });
    $.ajax({
        url: '/packages/' + type + '/' + pkg_id + '/action/get_package_files_list',
        type: 'GET',
        dataType: "json",
        contentType: "application/json;charset=utf-8",
        success: function (result) {
            //$('#modal_show_vim_body').empty();
            dialog.modal('hide');
            build_file_list("Files in " + pkg_id, result.files);
        },
        error: function (result) {
            dialog.modal('hide');
            bootbox.alert("An error occurred while retrieving the package content.");
        }
    });
}


function build_file_list(title, list) {
    $('#files_list_tbody').find('tr:gt(0)').remove();
    $('#files_list_tbody_title').text(title)
    for (var i in list) {
        var template = '<tr><td>-</td><td>' + list[i] + '</td><td><button type="button" class="btn btn-default" onclick="" disabled><i class="fa fa-folder-open"></i></button></td></tr>'
        $('#files_list_tbody').append(template)
    }
    $('#modal_files_list').modal('show');
}

