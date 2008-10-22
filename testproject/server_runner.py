# -*- coding: utf-8 -*-
__license__ = """
   Copyright (c) 2007 Mikeal Rogers
   Modified for RPGPedia project (c) 2008 by Almad

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied.
   See the License for the specific language governing permissions and
   limitations under the License.

"""


import sys, os
from time import sleep
from threading import Thread

import cherrypy

__all__ = ["ServerRunner"]

class ServerRunner(object):
    
    def __init__(self, port=8000):
        self.port = port
        self.httpd = None
        self.http_thread = None
    
    def run_server(self):
    
         import django.core.handlers.wsgi
         _application = django.core.handlers.wsgi.WSGIHandler()
    
         def application(environ, start_response):
             environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
             return _application(environ, start_response)
    
         import cherrypy
         httpd = cherrypy.wsgiserver.CherryPyWSGIServer(('', self.port), application, server_name='django-test-http')
         httpd_thread = Thread(target=httpd.start)
         httpd_thread.start()
         sleep(.5)
    
         self.httpd_thread = httpd_thread
         self.httpd = httpd
    
    def stop_server(self):
         self.httpd.stop()
