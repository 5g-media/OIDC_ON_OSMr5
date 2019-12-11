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
from packagehandler import views

urlpatterns = [
    url(r'(?P<package_type>\w+)/list$', views.show_packages, name='list_packages'),
    url(r'(?P<package_type>\w+)/create', views.create_package_empty, name='create_package_empty'),
    url(r'(?P<package_type>\w+)/(?P<package_id>[-\w]+)/delete$', views.delete_package, name='delete_package'),
    url(r'(?P<package_type>\w+)/(?P<package_id>[-\w]+)/clone', views.clone_package, name='clone_package'),
    url(r'(?P<package_type>\w+)/(?P<package_id>[-\w]+)/download', views.download_pkg, name='download_package'),
    url(r'(?P<package_type>\w+)/(?P<package_id>[-\w]+)/action/(?P<action_name>[-\w]+)', views.custom_action,
        name='custom_action'),
    url(r'(?P<package_type>\w+)/new$', views.onboard_package, name='onboard_package'),
]