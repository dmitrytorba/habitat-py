from dotenv import load_dotenv
from unificontrol import UnifiClient
import os

load_dotenv()

unifi = UnifiClient(
    host="net.ntreesolutions.com",
    port=443,
    cert=None,
    username=os.getenv("UNIFI_USER"),
    password=os.getenv("UNIFI_PASSWORD"),
    site=os.getenv("UNIFI_SITE"),
)

ipad97 = "d6:37:e3:73:12:b3"
ipad4g = "20:7d:74:43:d3:6c"


def block_tablets():
    unifi.block_client(ipad97)
    unifi.block_client(ipad4g)


def unblock_tablets():
    unifi.unblock_client(ipad97)
    unifi.unblock_client(ipad4g)


def get_clients():
    clients = unifi.list_clients()
    for client in clients:
        print(client["ip"])
        print(client["mac"])
    return clients


unblock_tablets()
