import json
import time

from dbt_rpc_client import DbtRpcClient

client = DbtRpcClient(host='localhost', port=8580)

data = client.snapshot(select=['model1', 'model2', 'model3', 'model1'])
print(json.dumps(data, indent=2))

resp = client.status()
print(resp)

# resp = client.test(an_arg="an_arg", a_second_arg="a_second_arg")
# token = resp.get("result").get("request_token")
# time.sleep(30)
# resp = client.poll(request_token=token)
# print(json.dumps(resp, indent=2))
