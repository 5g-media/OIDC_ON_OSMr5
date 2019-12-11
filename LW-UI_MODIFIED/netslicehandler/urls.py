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
from netslicehandler import views

urlpatterns = [
    url(r'templates/list$', views.list, name='list_templates'),
    url(r'templates/create', views.create_template, name='create_template'),
    url(r'templates/onboard', views.onboard_template, name='onboard_template'),
    url(r'templates/(?P<template_id>[-\w]+)/details', views.details, name='details'),
    url(r'templates/(?P<template_id>[-\w]+)/edit', views.edit, name='edit'),
    url(r'templates/(?P<template_id>[-\w]+)/delete', views.delete_template, name='delete_template'),
    url(r'templates/(?P<template_id>[-\w]+)/download', views.download_template, name='download_template'),
]