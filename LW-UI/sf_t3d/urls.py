#
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
#

from django.conf.urls import url, include
from authosm import views as user_views
from sf_t3d import views

app_name = 'base'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^home', views.home, name='home'),
    url(r'^auth/$', user_views.user_login, name='auth_user'),
    url(r'^projects/', include('projecthandler.urls.project', namespace='projects'), name='projects_base'),
    url(r'^sdn/', include('sdnctrlhandler.urls', namespace='sdns'), name='sdns_base'),
    url(r'^vims/', include('vimhandler.urls', namespace='vims'), name='vims_base'),
    url(r'^packages/', include('packagehandler.urls', namespace='packages'), name='packages_base'),
    url(r'^instances/', include('instancehandler.urls', namespace='instances'), name='instances_base'),
    url(r'^netslices/', include('netslicehandler.urls', namespace='netslices'), name='netslices_base'),
    url(r'^admin/users/', include('userhandler.urls', namespace='users'), name='users_base'),
    url(r'^forbidden', views.forbidden, name='forbidden'),

]
