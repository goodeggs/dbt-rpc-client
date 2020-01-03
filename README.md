# dbt-rpc-client
[![PyPI version](https://badge.fury.io/py/dbt-rpc-client.svg)](https://badge.fury.io/py/dbt-rpc-client)
![PyPI - Status](https://img.shields.io/pypi/status/dbt-rpc-client)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dbt-rpc-client)
![PyPI - License](https://img.shields.io/pypi/l/dbt-rpc-client)
[![Build Status](https://travis-ci.com/goodeggs/dbt-rpc-client.svg?branch=master)](https://travis-ci.com/goodeggs/dbt-rpc-client.svg?branch=master)

A python SDK for interacting with a [dbt rpc server](https://docs.getdbt.com/docs/rpc).

## Installation

```bash
$ pip install dbt-rpc-client
```

## Basic Usage

```python
from dbt_rpc_client import DbtRpcClient
import requests

rpc = DbtRpcClient(hostname="0.0.0.0", port=8580)

# Getting the current status of the dbt rpc server.
response = rpc.status()
assert isinstance(response, requests.Response)
assert response.ok

# Running dbt models via CLI command.
response = rpc.cli(cli_args="dbt run --models @model1 +model2+")
assert response.ok

# Running dbt models via `run` method.
response = rpc.run(models=["@model1", "+model2+"])
assert response.ok

# Polling a dbt rpc operation.
response = rpc.poll(request_token=response.get("id"))
assert response.ok
print(response.get("result").get("status"))

# Compiling/Running a SQL query.
sql = """
select 1
from {{ ref("my_dbt_model") }}
"""

response = rpc.compile_sql(sql=sql, name="my_sql_query")
assert response.ok

response = rpc.run_sql(sql=sql, name="my_sql_query")
assert response.ok
```

## Contributing

1. The first step to contributing is getting a copy of the source code. First, [fork `dbt-rpc-client` on GitHub](https://github.com/goodeggs/dbt-rpc-client/fork). Then, `cd` into the directory where you want your copy of the source code to live and clone the source code:

```bash
$ cd repos
$ git clone git@github.com:YourGitHubName/dbt-rpc-client.git
```

2. Now that you have a copy of the source code on your machine, create and activate a virtual envionment for `dbt-rpc-client`:

```bash
$ python3 -mvenv ~/.venvs/dbt-rpc-client
$ source ~/.venvs/dbt-rpc-client/bin/activate
```

2. Once inside the virtual environment, run `make dev_install` at the root of the repository:

```bash
$ (dbt-rpc-client) make dev_install
```

3. Run the [tox](https://tox.readthedocs.io/en/latest/) testing suite in the appropriate python environment to ensure things are working properly:
```bash
$ (dbt-rpc-client) tox -e py37
```

To format your code using [isort](https://github.com/timothycrosley/isort) and [flake8](http://flake8.pycqa.org/en/latest/index.html) before commiting changes, run the following commands:

```bash
$ (dbt-rpc-client) make isort
$ (dbt-rpc-client) make flake8
```

Once you've confirmed that your changes work and the testing suite passes, feel free to put out a PR!
