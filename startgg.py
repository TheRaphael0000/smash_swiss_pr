from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
import json

config = json.load(open("config.json"))
options = {
    "url": "https://api.start.gg/gql/alpha",
    "headers": {"Authorization": f"Bearer {config['start_gg_api_key']}"}
}

def request(query_path, replace={}):
    query = open(query_path).read()
    for k, v in replace.items():
        query = query.replace(str(k), str(v))
    transport = AIOHTTPTransport(**options)
    client = Client(transport=transport, fetch_schema_from_transport=True)
    data = client.execute(gql(query))
    return data

