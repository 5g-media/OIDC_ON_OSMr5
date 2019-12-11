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
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
import urllib


# Create your views here.
def user_login(request):

    logout(request)

    error_message = ''
    if request.POST:
        print request.POST.get('username')
        print request.POST.get('password')
        next_page = request.POST.get('next')
        next_page = urllib.unquote(next_page).decode('iso-8859-2')
        try:
            user = authenticate(username=request.POST.get('username'),
                                password=request.POST.get('password'),
                                project_id=request.POST.get('project_id'))
        except Exception as e:
            print e
            res = HttpResponseRedirect('/auth')
            res.set_cookie('logout_reason', '', max_age=10)
            return res

        if user and user.is_active:
            if user.is_authenticated:
                login(request, user)
                request.session['projects'] = user.get_projects()
                if next_page == "" or next_page is None:
                    return HttpResponseRedirect('/home')
                else:
                    return HttpResponseRedirect(next_page)
        else:
            error_message = 'Login failed!'
    return render(request, 'login.html', {'error_message': error_message, 'collapsed_sidebar': False})
