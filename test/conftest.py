import json
import logging
import os
from pathlib import Path

import pytest
import yaml

from tycho.client import TychoClientFactory
from tycho.core import Tycho

# https://medium.com/@yeraydiazdiaz/what-the-mock-cheatsheet-mocking-in-python-6a71db997832

modify_data_path = os.path.dirname(os.path.abspath(__file__))
modify_data_abs_path = os.path.join(modify_data_path, "../tycho", "json")

logger = logging.getLogger(__name__)


def get_sample_spec(name):
    """ Load a docker-compose specification from our samples. """
    result = None
    d = os.path.dirname(__file__)
    sample_path = os.path.join(d, "../tycho", "sample", name, "docker-compose.yaml")
    with open(sample_path, "r") as stream:
        result = yaml.load(stream)
    return result


def make_request():
    """ Create a Tycho request object to test with. """
    request = {
        "name": "test",
        "principal": '{"username": "renci"}',
        "env": {},
        "system": get_sample_spec("jupyter-ds"),
        "services": {
            "jupyter-datascience": {
                "port": "8888",
                "clients": ["127.0.0.1"]
            }
        }
    }
    return request


@pytest.fixture(scope='module')
def system_request():
    return make_request()


@pytest.fixture(scope='module')
def system(system_request):
    """ Create a Tycho request object to test with. """
    tycho = Tycho(backplane='kubernetes')
    print(f"{json.dumps(system_request, indent=2)}")
    return tycho.parse(system_request)


@pytest.fixture(scope='module')
def client():
    return TychoClientFactory().get_client()


@pytest.fixture(params=["data1", "data2"])
def volume_model_data(request):
    if request.param is "data1":
        data = [{
            "name": "nginx",
            "image": "sample/image:v1",
            "command": "some entrypoint",
            "env": [],
            "limits": [],
            "requests": {},
            "ports": [],
            "expose": [],
            "depends_on": [],
            "volumes": ["pvc://nfsrods/rods:/home/rods", "pvc://cloud-top:/home/shared"]
        }]
        return data
    if request.param is "data2":
        data = [
            {'container_name': 'nginx',
             'pvc_name': 'nfsrods',
             'volume_name': 'nfsrods',
             'path': '/home/rods',
             'subpath': 'rods'
             },
            {'container_name': 'nginx',
             'pvc_name': 'cloud-top',
             'volume_name': 'cloud-top',
             'path': '/home/shared',
             'subpath': ''
             }
        ]
        return data


@pytest.fixture
def mock_modify_function_env_variables(mocker):
    mocker.patch.dict("os.environ", {"NAMESPACE": os.environ.get("NAMESPACE", "default")})
    yield


def get_data_for_modify_function():
    data_list = []
    files = Path(modify_data_abs_path).glob("*.json")
    for file in files:
        with open(file) as data_file:
            data_list.append(data_file.read())
    return data_list


@pytest.fixture(params=get_data_for_modify_function())
def modify_data(request):
    data = json.loads(request.param)
    yield data
