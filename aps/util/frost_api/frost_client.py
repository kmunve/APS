import json


def get_client_id():
    """
    Requires a file "client_id.json" with the following content:
    {"client_id":  "12493b54-c073-4c44-7a41-633a3569f636"}

    :return:
    """
    with open("client_id.json") as file:
        _id = json.load(file)
        return _id["client_id"]
