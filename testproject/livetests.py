#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Run webtests """

import sys
import os, os.path

from django.core.management import setup_environ
import nose
from nose.config import Config, all_config_files
from nose.plugins.manager import DefaultPluginManager

import settings
setup_environ(settings)

from server_runner import ServerRunner

def run_selenium_tests():
    
        # nose config
        config = Config(files=all_config_files(), plugins=DefaultPluginManager())
        config.workingDir = os.path.join(os.path.dirname(__file__)) 
        server_runner = ServerRunner()
        server_runner.run_server()
        success = nose.run(config=config)
        server_runner.stop_server()
        
        return success

def main():
    success = run_selenium_tests()
    
    sys.exit(not success)
    
if __name__ == '__main__':
    main()
