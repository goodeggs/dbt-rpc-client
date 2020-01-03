import pytest

from dbt_rpc_client import DbtRpcClient


@pytest.fixture(scope='session')
def client():
    return DbtRpcClient(host="0.0.0.0", port=8580)
