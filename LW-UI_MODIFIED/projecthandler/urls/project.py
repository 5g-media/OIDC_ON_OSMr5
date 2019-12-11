#
#   Copyright 2017 CNIT - Consorzio Nazionale Interuniversitario per le Telecomunicazioni
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an  BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#

from django.conf.urls import url, include
from projecthandler import views

urlpatterns = [
    url(r'^$', views.open_project, name='open_project'),
    url(r'^list/', views.user_projects, name='projects_list'),
    url(r'^new/', views.create_new_project, name='new_project'),
    url(r'^descriptors/', include('descriptorhandler.urls', namespace='descriptors'), name='descriptor_base'),
    url(r'^(?P<project_id>[\w ]+)/delete$', views.delete_project, name='delete_project'),
    url(r'^(?P<project_id>[\w ]+)/switch', views.switch_project, name='switch_project'),
    url(r'^(?P<project_id>[\w ]+)/edit', views.edit_project, name='edit_project'),





]