import json
import uuid
from typing import Dict, List

import attr
import requests

from .version import __version__


@attr.s
class DbtRpcClient(object):

    host: str = attr.ib(default="0.0.0.0")
    port: int = attr.ib(default=8580)
    jsonrpc_version: str = attr.ib(default="2.0")
    url: str = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.url = f"http://{self.host}:{self.port}/jsonrpc"

    def _construct_headers(self) -> Dict:
        '''Constructs a standard set of headers for HTTP requests.'''
        headers = requests.utils.default_headers()
        headers["User-Agent"] = f"dbt-rpc-client/{__version__}"
        headers["Content-Type"] = "application/json"
        return headers

    def _post(self, data: Dict = None) -> Dict:
        '''Constructs a standard way of making
        a POST request to the dbt RPC server.
        '''
        headers = self._construct_headers()
        response = requests.post(self.url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()

    def _default_request(self, method: str) -> Dict:
        data = {
            "jsonrpc": self.jsonrpc_version,
            "method": method,
            "id": str(uuid.uuid1())
        }
        return data

    def status(self) -> Dict:
        data = self._default_request(method='status')
        return self._post(data=json.dumps(data))

    def poll(self, request_token: str, logs: bool = False, logs_start: int = 0) -> Dict:
        data = self._default_request(method='poll')
        data["params"] = {
            "request_token": request_token,
            "logs": logs,
            "logs_start": logs_start
        }
        return self._post(data=json.dumps(data))

    def ps(self, completed: bool = False) -> Dict:
        'Lists running and completed processes executed by the RPC server.'
        data = self._default_request(method='ps')
        data["params"] = {
            "completed": completed
        }
        return self._post(data=json.dumps(data))

    def kill(self, task_id: str) -> Dict:
        'Terminates a running RPC task.'
        data = self._default_request(method='kill')
        data["params"] = {
            "task_id": task_id
        }
        return self._post(data=json.dumps(data))

    def cli(self, cli_args: str, **kwargs) -> Dict:
        'Terminates a running RPC task.'
        data = self._default_request(method='cli_args')
        data["params"] = {
            "cli_args": cli_args,
            "task_tags": kwargs
        }
        return self._post(data=json.dumps(data))

    def compile(self, models: List[str] = None, exclude: List[str] = None, **kwargs) -> Dict:
        'Runs a dbt compile command.'
        data = self._default_request(method='compile')

        if models is not None:
            data["params"]["models"] = ' '.join(models)

        if exclude is not None:
            data["params"]["exclude"] = ' '.join(exclude)

        if kwargs is not None:
            data["params"]["task_tags"] = kwargs

        return self._post(data=json.dumps(data))

    def run(self, models: List[str] = None, exclude: List[str] = None, **kwargs) -> Dict:
        'Runs a dbt run command.'
        data = self._default_request(method='run')

        if models is not None:
            data["params"]["models"] = ' '.join(models)

        if exclude is not None:
            data["params"]["exclude"] = ' '.join(exclude)

        if kwargs is not None:
            data["params"]["task_tags"] = kwargs

        return self._post(data=json.dumps(data))
