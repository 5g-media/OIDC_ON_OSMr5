#   Copyright 2018 EveryUP Srl
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


from django.conf.urls import url
from descriptorhandler import views

urlpatterns = [
    url(r'(?P<descriptor_type>\w+)/(?P<descriptor_id>[-\w]+)(/$)', views.edit_descriptor, name='edit_descriptor'),
    url(r'(?P<descriptor_type>\w+)/(?P<descriptor_id>[-\w]+)/addElement/(?P<element_type>\w+)', views.addElement,
        name='addElement'),
    url(r'(?P<descriptor_type>\w+)/(?P<descriptor_id>[-\w]+)/removeElement/(?P<element_type>\w+)', views.removeElement,
        name='removeElement'),
    url(r'(?P<descriptor_type>\w+)/(?P<descriptor_id>[-\w]+)/updateElement/(?P<element_type>\w+)', views.updateElement,
        name='updateElement'),
    url(r'(?P<descriptor_type>\w+)/(?P<descriptor_id>[-\w]+)/action/(?P<action_name>[-\w]+)', views.custom_action,
        name='custom_action'),
    url(r'composer$', views.open_composer, name='open_composer'),
    url(r'availablenodes', views.get_available_nodes, name='get_available_nodes'),
]
