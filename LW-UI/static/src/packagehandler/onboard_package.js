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

function create(fs, dropzone) {
    var id = $('.nav-tabs .active').attr('id');
    if (dropzone) id = 'file_li';
    var type, text;
    var data = new FormData();
    switch (id) {

        case 'file_li':
            type = 'file';

            var files = dropzone ? fs : document.getElementById('js-upload-files').files;
            if (!files || !files.length) {
                files = document.getElementById('drop-zone').files;
                if (!files || !files.length) {
                    alert("Select a file");
                    return
                }
            }
            console.log(files[0])
            var patt1 = /\.([0-9a-z]+)(?:[\?#]|$)/i;
            console.log(files[0].name.match(patt1));
            var extension = files[0].name.substr(files[0].name.lastIndexOf('.') + 1);
            console.log(extension);
            if (!(extension == 'gz' )) {
                alert("The file must be .tar.gz");
                return
            }

            data.append('file', files[0]);
            break;
    }
    data.append('csrfmiddlewaretoken', csrf_token);
    data.append('type', type);
    data.append('text', text);
    data.append('id', '{{descriptor_id}}');
    console.log(text);
    var dialog = bootbox.dialog({
                message: '<div class="text-center"><i class="fa fa-spin fa-spinner"></i> Onboarding...</div>',
                closeButton: true
            });
    $.ajax({
        url: new_desc_url,
        type: 'POST',
        data: data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (result) {
            dialog.modal('hide');
            refreshTable();
        },
        error: function (result) {
            dialog.modal('hide');
            showAlert(result);
        }
    });
}