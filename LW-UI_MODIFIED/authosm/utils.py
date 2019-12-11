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

import time
import authosm.models


def get_user(request):
    user = authosm.models.OsmUser.objects.get(username=request.session['_auth_user_id'])
    return user


def is_token_valid(token):

    expiration = token['expires'] if 'expires' in token \
                                     and isinstance(token['expires'], (int, long, float, complex)) else None
    if expiration is None:
        return False

    return expiration > time.time()
