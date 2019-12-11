/*
   Copyright 2019 EveryUP srl

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

var dropZone = document.getElementById('drop-zone');
dropZone.ondrop = function (e) {
    e.preventDefault();
    this.className = 'upload-drop-zone';
    create(e.dataTransfer.files, true);
};

dropZone.ondragover = function () {
    this.className = 'upload-drop-zone drop';
    return false;
};

dropZone.ondragleave = function () {
    this.className = 'upload-drop-zone';
    return false;
};