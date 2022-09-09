from unittest import mock
import pytest
from tycho.tycho_utils import Resource
import os

class TestResource:

    testdata = [
        ("test.yaml", None, "yaml"),
        ("test.yaml", 'yaml', "yaml"),
        ("test.json", None, "json"),
        ("test.json", 'json', "json"),
        ("test", 'yaml', "yaml"),
        ("test.exe", None, "json"),
    ]

    @pytest.mark.parametrize("resource_name,format,correct_type", testdata)
    def test_get_resource_obj(resource_name, format, correct_type):
        # Set up mocks
        mock.patch('tycho.tycho_utils.Resource.get_resource_path', "")
        mock.patch('os.path.exists', True)
        mock.patch('tycho.tycho_utils.Resource.load_json', "json")
        mock.patch('tycho.tycho_utils.Resource.load_yaml', "yaml")

        # Test get_resource_obj
        resource = Resource()
        result = resource.get_resource_obj(resource_name, format)
        assert result == correct_type
