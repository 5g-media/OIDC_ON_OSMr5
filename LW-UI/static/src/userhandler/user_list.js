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

function openModalCreateUser(args) {

    select2_groups = $('#projects').select2({
        placeholder: 'Select Projects',
        width: '100%',
        ajax: {
            url: args.projects_list_url,
            dataType: 'json',
            processResults: function (data) {
                projects = [];
                if (data['projects']) {
                    for (d in data['projects']) {
                        var project = data['projects'][d];
                        projects.push({id: project['_id'], text: project['name']})
                    }
                }

                return {
                    results: projects
                };
            }
        }
    });

    $('#modal_new_user').modal('show');
}

function openModalEditUser(args) {
    var url = '/admin/users/' + args.user_id;
    var user_projects = args.projects ? args.projects.split(',') : [];
    $("#formEditUser").attr("action", url);
    $("#projects_old").val(user_projects.toString());
    $('#projects_edit').val(null).trigger('change');
    $('#default_project_edit').val(null).trigger('change');
    $('#edit_password').val('');
    if (user_projects.length > 0) {
            // Create a DOM Option and pre-select by default
            var newOption = new Option(user_projects[0], user_projects[0], true, true);
            // Append it to the select
            $('#default_project_edit').append(newOption).trigger('change');

        for (var d in user_projects) {
            var project = user_projects[d];
            // Create a DOM Option and pre-select by default
            var newOption = new Option(project, project, true, true);
            // Append it to the select
            $('#projects_edit').append(newOption).trigger('change');
        }

    }


    $('#modal_edit_user').modal('show');
}

function deleteUser(user_id, name) {
    var delete_url = '/admin/users/' + user_id + '/delete';
    bootbox.confirm("Are you sure want to delete " + name + "?", function (confirm) {
        if (confirm) {
            var dialog = bootbox.dialog({
                message: '<div class="text-center"><i class="fa fa-spin fa-spinner"></i> Loading...</div>',
                closeButton: false
            });
            $.ajax({
                url: delete_url,
                dataType: "json",
                contentType: "application/json;charset=utf-8",
                success: function (result) {
                    //$('#modal_show_vim_body').empty();
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