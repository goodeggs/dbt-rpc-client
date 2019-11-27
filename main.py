from dbt_rpc_client import DbtRpcClient

client = DbtRpcClient(host='localhost', port=8580)

#resp = client.compile()
#resp = client.cli(cli_args="dbt debug")
resp = client.run_sql(sql="select {{ 1 + 1 }} as id", name="my_query")
print(resp)
