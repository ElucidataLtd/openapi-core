import json
import pytest

from openapi_core.shortcuts import create_spec
from openapi_core.validation.request.validators import RequestValidator
from openapi_core.validation.response.validators import ResponseValidator
from openapi_core.wrappers.mock import MockRequest, MockResponse


class TestAdditionalProperties(object):

    spec_path = "data/v3.0/additional_properties.yaml"
    server = "http://localhost"

    @pytest.fixture
    def spec_dict(self, factory):
        return factory.spec_from_file(self.spec_path)

    @pytest.fixture
    def spec(self, spec_dict):
        return create_spec(spec_dict)

    @pytest.fixture
    def request_validator(self, spec):
        return RequestValidator(spec)

    @pytest.fixture
    def response_validator(self, spec):
        return ResponseValidator(spec)

    def test_any_additional_property(self, response_validator):
        request = MockRequest(self.server, "get", "/anything")
        data_json = {
            'data': [],
            "test": True,
            "something": "else",
        }
        data = json.dumps(data_json)
        response = MockResponse(data)

        response_result = response_validator.validate(request, response)
        assert not response_result.errors, response_result.errors

    @pytest.mark.xfail(
        reason="Valdation on additional properties does not seem to validate"
    )
    def test_string_additional_property_invalid(self, response_validator):
        request = MockRequest(self.server, "get", "/strings-only")
        data_json = {
            'data': [],
            "test": True,
            "something": "else",
        }
        data = json.dumps(data_json)
        response = MockResponse(data)

        response_result = response_validator.validate(request, response)
        assert response_result.errors, "expected errors"

    def test_string_additional_property(self, response_validator):
        request = MockRequest(self.server, "get", "/strings-only")
        data_json = {
            'data': "test",
            "test": "test",
            "something": "else",
        }
        data = json.dumps(data_json)
        response = MockResponse(data)

        response_result = response_validator.validate(request, response)
        assert not response_result.errors, response_result.errors
