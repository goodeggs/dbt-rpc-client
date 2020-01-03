import base64
import json
import platform
import sys
import uuid
from typing import Dict, List

import attr
import requests

from .version import __version__


@attr.s
class DbtRpcClient(object):

    host: str = attr.ib(default="0.0.0.0")
    port: int = attr.ib(validator=attr.validators.instance_of(int), default=8580)
    jsonrpc_version: str = attr.ib(validator=attr.validators.instance_of(str), default="2.0")
    url: str = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.url = f"http://{self.host}:{self.port}/jsonrpc"

    @staticmethod
    def _construct_user_agent() -> str:
        '''Constructs a standard User Agent string to be used in headers for HTTP requests.'''
        client = f"dbt-rpc-client/{__version__}"
        python_version = f"Python/{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        system_info = f"{platform.system()}/{platform.release()}"
        user_agent = " ".join([python_version, client, system_info])
        return user_agent

    def _construct_headers(self) -> Dict:
        '''Constructs a standard set of headers for HTTP requests.'''
        headers = requests.utils.default_headers()
        headers["User-Agent"] = self._construct_user_agent()
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"
        return headers

    def _post(self, data: str = None) -> requests.Response:
        '''Constructs a standard way of making a POST request to the dbt RPC server.'''
        headers = self._construct_headers()
        response = requests.post(self.url, headers=headers, data=data)
        response.raise_for_status()
        return response

    def _default_request(self, method: str) -> Dict:
        data = {
            "jsonrpc": self.jsonrpc_version,
            "method": method,
            "id": str(uuid.uuid1()),
            "params": {}
        }
        return data

    def _selection(self, *, models: List[str] = None, select: List[str] = None, exclude: List[str] = None) -> Dict:
        params = {}
        if models is not None:
            params["models"] = ' '.join(set(models))
        if select is not None:
            params["select"] = ' '.join(set(select))
        if exclude is not None:
            params["exclude"] = ' '.join(set(exclude))

        return params

    def status(self) -> requests.Response:
        data = self._default_request(method='status')
        return self._post(data=json.dumps(data))

    def poll(self, *, request_token: str, logs: bool = False, logs_start: int = 0) -> requests.Response:
        data = self._default_request(method='poll')
        data["params"] = {
            "request_token": request_token,
            "logs": logs,
            "logs_start": logs_start
        }
        return self._post(data=json.dumps(data))

    def ps(self, *, completed: bool = False) -> requests.Response:
        'Lists running and completed processes executed by the RPC server.'
        data = self._default_request(method='ps')
        data["params"] = {
            "completed": completed
        }
        return self._post(data=json.dumps(data))

    def kill(self, *, task_id: str) -> requests.Response:
        'Terminates a running RPC task.'
        data = self._default_request(method='kill')
        data["params"] = {
            "task_id": task_id
        }
        return self._post(data=json.dumps(data))

    def cli(self, *, cli_args: str, **kwargs) -> requests.Response:
        'Terminates a running RPC task.'
        data = self._default_request(method='cli_args')
        data["params"] = {
            "cli_args": cli_args
        }

        if kwargs is not None:
            data["params"]["task_tags"] = kwargs

        return self._post(data=json.dumps(data))

    def compile(self, *, models: List[str] = None, exclude: List[str] = None, **kwargs) -> requests.Response:
        'Runs a dbt compile command.'
        data = self._default_request(method='compile')
        data["params"].update(self._selection(models=models, exclude=exclude))

        if kwargs is not None:
            data["params"]["task_tags"] = kwargs

        return self._post(data=json.dumps(data))

    def run(self, *, models: List[str] = None, exclude: List[str] = None, **kwargs) -> requests.Response:
        'Runs a dbt run command.'
        data = self._default_request(method='run')
        data["params"].update(self._selection(models=models, exclude=exclude))

        if kwargs is not None:
            data["params"]["task_tags"] = kwargs

        return self._post(data=json.dumps(data))

    def snapshot(self, *, select: List[str] = None, exclude: List[str] = None, **kwargs) -> requests.Response:
        'Runs a dbt snapshot command.'
        data = self._default_request(method='snapshot')
        data["params"].update(self._selection(select=select, exclude=exclude))

        if kwargs is not None:
            data["params"]["task_tags"] = kwargs

        return self._post(data=json.dumps(data))

    def test(self, *, models: List[str] = None, exclude: List[str] = None, data: bool = True, schema: bool = True, **kwargs) -> requests.Response:
        payload = self._default_request(method='test')
        payload["params"] = {
            "data": data,
            "schema": schema
        }

        payload["params"].update(self._selection(models=models, exclude=exclude))

        if kwargs is not None:
            payload["params"]["task_tags"] = kwargs

        return self._post(data=json.dumps(payload))

    def seed(self, *, show: bool = False, **kwargs) -> requests.Response:
        data = self._default_request(method='seed')
        data["params"] = {
            "show": show
        }

        if kwargs is not None:
            data["params"]["task_tags"] = kwargs

        return self._post(data=json.dumps(data))

    def generate_docs(self, *, models: List[str] = None, exclude: List[str] = None, compile: bool = False, **kwargs) -> requests.Response:
        data = self._default_request(method='docs.generate')
        data["params"] = {
            "compile": compile
        }

        data["params"].update(self._selection(models=models, exclude=exclude))

        if kwargs is not None:
            data["params"]["task_tags"] = kwargs

        return self._post(data=json.dumps(data))

    def run_operation(self, *, macro: str) -> requests.Response:
        data = self._default_request(method='run-operation')
        data["params"] = {
            "macro": macro
        }
        return self._post(data=json.dumps(data))

    def compile_sql(self, *, sql: str, name: str, timeout: int = 60) -> requests.Response:
        data = self._default_request(method='compile_sql')
        data["params"] = {
            "sql": str(base64.b64encode(bytes(sql, 'utf-8'))),
            "timeout": timeout,
            "name": name
        }
        return self._post(data=json.dumps(data))

    def run_sql(self, *, sql: str, name: str, timeout: int = 60) -> requests.Response:
        data = self._default_request(method='run_sql')
        data["params"] = {
            "sql": str(base64.b64encode(bytes(sql, 'utf-8'))),
            "timeout": timeout,
            "name": name
        }
        return self._post(data=json.dumps(data))
