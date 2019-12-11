# -*- coding: utf-8 -*-

"""
AuthconnOIDC implements the connector for OpenID Connect protocol,
Authorization Code flow and Implicit flow, to bring it for OSM.
"""


from authconn import Authconn, AuthException, AuthconnOperationException

import jwt
from time import time
import requests
import jwt
import urllib.request
import json
import base64
import logging
from http import HTTPStatus


class AuthconnOIDC(Authconn):
    def __init__(self, config):
        Authconn.__init__(self, config)
        self.logger = logging.getLogger("nbi.authenticator.oidc")

    
 
