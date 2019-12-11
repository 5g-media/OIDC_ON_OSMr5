from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from settings import OIDC_CALLBACK

def access_token(request):
    
    code = request.GET.get('code','')
    print code

    try:
        user = authenticate(username='',
                            password='',
                            project_id=None,
                            code=code,
                            redirect_url = OIDC_CALLBACK,
                            grant_type = 'authorization_code')
    except Exception as e:
        print e
        res = HttpResponseRedirect('/auth')
        res.set_cookie('logout_reason', '', max_age=10)
        return res

    if user and user.is_active:
        if user.is_authenticated:
            login(request, user)
            request.session['projects'] = user.get_projects()
            
    response = redirect('projects:open_project')
    #request.user.is_authenticated.value = True
    return response

