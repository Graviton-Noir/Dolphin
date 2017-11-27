#!/usr/bin/env python3
from base64 import b64encode
from json import dumps, loads

from httplib2 import Http


class Client:

    def __init__(self):
        self.http = Http(".cache", disable_ssl_certificate_validation=True)
        user_password = b64encode(b"epita_user_3:dolphin41331").decode("ascii")
        self.headers = {'Authorization': 'Basic %s' % user_password}
        self.url = "https://dolphin.jump-technology.com:3389/api/v1/"

    def put_portfolio(self, id, body):
        return self.http.request("{}portfolio/{}/dyn_amount_compo".format(self.url, id),
                                 "PUT",
                                 headers=self.headers,
                                 body=dumps(body))

    def get_portfolio(self, id):
        return self.http.request("{}portfolio/{}/dyn_amount_compo".format(self.url, id),
                                 "GET",
                                 headers=self.headers)


def bytes_to_json(bytes):
    # to double quotes to make it valid JSON
    my_json = bytes.decode('utf8').replace("'", '"')
    # Load the JSON to a Python list & dump it back out as formatted JSON
    data = loads(my_json)
    return data


if __name__ == '__main__':
    client = Client()
    default_id = 595
    group_id = 576

    # get the default portfolio
    #content = client.get_portfolio(default_id)
    # replace PORTFOLIO_USER_REF by PORTFOLIO_USER3
    #content = content.replace(b'PORTFOLIO_USER_REF', b'PORTFOLIO_USER3')
    # convert bytes to json
    #json = bytes_to_json(content)
    json =
    client.put_portfolio(group_id, json)
