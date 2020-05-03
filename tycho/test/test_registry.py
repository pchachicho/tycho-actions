import os
import json
import logging
import pytest
import requests
import traceback
import yaml
from string import Template
from tycho.context import Principal, TychoContext

logger = logging.getLogger (__name__)
#logger.setLevel (logging.INFO)

def get_registry (file_name):
    registry = {}
    registry_config = os.path.join (
        os.path.dirname (os.path.dirname (__file__)),
        "conf", file_name)
    with open(registry_config, 'r') as stream:
        registry = yaml.safe_load (stream)
    return registry

def test_registry (caplog):
    caplog.set_level(logging.INFO, __name__)
    registry = get_registry ("app-registry.yaml")
    registry_id = registry.get('metadata',{}).get ('id', None)    
    logger.info (f"processing app registry: {registry_id}")
    
    repository_context = { r['id'] : r['url'] for r in registry.get('repositories', []) }
    logger.info (f"repository context: {repository_context}")

    registries = registry.get ('registries', [])
    for registry in registries:
        registry_id = registry['id']
        logger.info (f"processing registry id:{registry_id} name:{registry['name']}")
        for app in registry.get ('apps', []):
            app_id = app['id']
            for key in [ 'spec', 'icon', 'docs' ]:
                url = app [key]
                url = Template(url).safe_substitute (repository_context)
                response = None
                try:
                    response = requests.get (url)
                    if response is not None:
                        if response.status_code == 200:
                            logger.info (f"  -- validated {key} for url {url}")
                        else:
                            logger.error (f"  ++ unable to get {key} for {app_id} at {url}")
                except Exception as e:
                    if response is not None:
                        if response.status_code != 200:
                            logger.info (f"  ++ unable to get {key} for {app_id}; status: {response.status_code} for {url}")
                    else:
                        logger.error (f"  ++ unable to get {key} for {app_id} at {url}")

#def test_context (caplog):
def test_context ():
#    caplog.set_level(logging.INFO, __name__)
    principal = Principal (username="test_user")
    seen = {}
    failed = []
    for product in [ "braini", "catalyst", "scidas" ]:
        tc = TychoContext (product=product)
        #logger.info (f"--tycho-context.apps: {json.dumps(tc.apps, indent=2)}")
        apps = list(tc.apps.items ())
        for app_id, app in apps:
            try:
                if app_id in seen:
                    logger.info (f"-- skipping seen app {app_id}")
                    continue
                seen [app_id] = app_id
                system = tc.start (principal=principal,
                                   app_id=app_id)
                logger.info (f""">> f"https://<UX_URL>/private/{app_id}/{principal.username}/{system.identifier}/ """)
            except Exception as e:
                logger.error (f"App {app_id} failed. {e}")
                traceback.print_exc ()
                failed.append (app_id)
    fail_list = "\n==    * ".join (failed)
    logger.error (f"""
=================================
== The following apps failed:
==    * {fail_list}
=================================""")