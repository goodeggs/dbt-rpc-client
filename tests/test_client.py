import pytest


def test_client_url(client):
    assert client.url == "http://0.0.0.0:8580/jsonrpc"


@pytest.mark.parametrize('method', ['status', 'poll', 'kill', 'cli_args'])
def test_default_request(client, method):
    expected = {
        "jsonrpc": client.jsonrpc_version,
        "method": method,
        "params": {}
    }
    resp = client._default_request(method=method)
    assert resp["jsonrpc"] == expected["jsonrpc"]
    assert resp["method"] == expected["method"]
    assert resp["params"] == expected["params"]
