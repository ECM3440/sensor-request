from dataclasses import dataclass

import mock
import pytest
from pytest_httpserver import HTTPServer
from ...main.azure_iot.azure_iot_hub import IoTHubClient


@pytest.fixture(scope="session")
def httpserver_listen_address():
    return ("127.0.0.1", 5000)


def setup_test_server(httpserver: HTTPServer):
    httpserver.expect_request("/create_sensor").respond_with_data("Success")


@mock.patch("src.main.azure_iot.azure_iot_hub.IoTHubClient.create_device_client")
@mock.patch("src.main.azure_iot.azure_iot_hub.IoTHubDeviceClient")
def test_post(
    mock_create_device_client, mock_iot_hub_device_client, httpserver: HTTPServer
):
    # check that the server is called with the correct request
    iot_hub_client = IoTHubClient(
        device_name="device name", connection_str="connection string"
    )

    httpserver.expect_request("/test").respond_with_data("Success")

    code = iot_hub_client.post("/test", {"test": "testing testing, one two, one two"})

    assert code == 200


@mock.patch(
    "src.main.azure_iot.azure_iot_hub.IoTHubDeviceClient.create_from_connection_string"
)
def test_create_device_client(mock_create_from_connection_string):
    iot_hub_client = IoTHubClient(
        device_name="device name", connection_str="connection string"
    )

    iot_hub_client.create_device_client()

    assert mock_create_from_connection_string.call_count == 2


@mock.patch(
    "src.main.azure_iot.azure_iot_hub.IoTHubClient.create_device_client",
)
@mock.patch(
    "src.main.azure_iot.azure_iot_hub.MethodResponse.create_from_method_request"
)
@mock.patch("src.main.azure_iot.azure_iot_hub.IoTHubDeviceClient.send_method_response")
def test_set_request_handler(
    mock_create_device_client,
    mock_create_from_method_request,
    mock_send_method_response,
):
    iot_hub_client = IoTHubClient(
        device_name="device name", connection_str="connection string"
    )

    assert mock_send_method_response.call_count == 1
