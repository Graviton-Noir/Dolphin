#!/usr/bin/env python

from base64 import b64encode
from json import dumps, loads
from httplib2 import Http
from asset import Asset
from util import string_result_to_float

SHARPE = '20'
PORTFOLIO_ID = '576'


class Client:

    def __init__(self):
        self.http = Http(disable_ssl_certificate_validation=True)
        user_password = b64encode(b"epita_user_3:dolphin41331").decode("ascii")
        self.headers = {'Authorization': 'Basic %s' % user_password}
        self.url = "https://dolphin.jump-technology.com:3389/api/v1/"
        self.currency_rates_dict = None

    def get_ratio(self):
        response, content = self.http.request("{}ratio".format(self.url),
                                              "GET",
                                              headers=self.headers)
        return response, content

    def put_portfolio(self, body):
        return self.http.request("{}portfolio/576/dyn_amount_compo".format(self.url),
                                 "PUT",
                                 headers=self.headers,
                                 body=dumps(body))

    # Put portfolio from given assets list (json string)
    def put_portfolio_from_assets(self, portfolio_json):
        body = {
            "label": "PORTFOLIO_USER3",
            "currency": {
                "code": "EUR"
            },
            "type": "front",
            "values": {
                "2012-01-01": loads(portfolio_json)
            }
        }
        return self.http.request("{}portfolio/576/dyn_amount_compo".format(self.url),
                                 "PUT",
                                 headers=self.headers,
                                 body=dumps(body))

    def get_portfolio(self):
        return self.http.request("{}portfolio/576/dyn_amount_compo".format(self.url),
                                 "GET",
                                 headers=self.headers)

    def post_ratio_invoke(self, ratio, asset, benchmark, start_date, end_date):
        body = {
            "ratio": ratio,
            "asset": asset,
            "benchmark": benchmark,
            "start_date": start_date,
            "end_date": end_date,
            "frequency": "null"
        }
        return self.http.request("{}ratio/invoke".format(self.url),
                                 "POST",
                                 headers=self.headers,
                                 body=dumps(body))


    #By Axel
    def get_all_caract(self, assets):
        string = '{"ratio": [15, 17, 18, 19, 20, 21, 22, 29], "asset": [], "bench": "null", "start_date": "2012-01-01", "end_date": "2017-06-30", "frequency": "null"}'
        body = loads(string)
        for item in assets:
            body["asset"].append(item)
        return self.http.request("{}ratio/invoke".format(self.url),
                "POST",
                headers=self.headers,
                body =dumps(body))


    def get_asset_quote(self, id, start_date, end_date):
        return self.http.request("{}asset/{}/quote?start_date={}&end_date={}".format(self.url, id,
                                                                                     start_date, end_date),
                                 "GET",
                                 headers=self.headers)

    # Convert price string to amount in given currency
    def price_str_to_amount(self, s, to_currency):
        # Ex : 25 USD
        # Currency (ex : USD)
        # Amount = 25
        amount, currency = s.split()
        amount = amount.replace(',', '.')
        t = self.get_currency_rates_dict(True)[currency][to_currency]
        return float(amount) * float(t)


        #By Axel
    def fill_all_assets(self):
        response, content = self.get_all_assets()
        json_content = loads(content)
        assets = []
        for assets_ids in json_content:
            assets.append(int(assets_ids["ASSET_DATABASE_ID"]['value']))
        response, content = self.get_all_caract(assets)
        result = []  # tab of assets
        json_content2 = loads(content)
        for i in range(0, len(json_content) -1):
            asset = json_content[i]
            #Format "55,55 EUR"
            last_close_value = asset["LAST_CLOSE_VALUE"]["value"]
            #last_close_value_in_curr = asset["LAST_CLOSE_VALUE_IN_CURR"]["value"]
            eur_last_close_value = self.price_str_to_amount(last_close_value, 'EUR')
            label = asset["LABEL"]["value"]
            the_id = asset["ASSET_DATABASE_ID"]["value"]  # ID

            #result from get_all_caract()
            asset = json_content2[the_id]
            volatility = asset["18"]["value"]
            sharpe = string_result_to_float(asset["20"]["value"])
            rendement = asset["21"]["value"]
            rendement_annuel = asset["17"]["value"]
            variance_historique = asset["22"]["value"]
            a = Asset(the_id, label, eur_last_close_value, last_close_value,
                volatility, sharpe, rendement, rendement_annuel,
                variance_historique)
            result.append(a)
        return result

    # return results and assets_dict
    def fill_all_assets_split(self):
        assets_dict = {}  # Assets dictionary
        assets_results = self.fill_all_assets()
        for a in assets_results:
            assets_dict[a.id] = a
        return assets_results, assets_dict

    def get_all_assets(self):
        return self.http.request(
            "{}asset?CURRENCY=EUR&TYPE=STOCK&columns=ASSET_DATABASE_ID&columns=TYPE&columns=LAST_CLOSE_VALUE&columns=LABEL&date=2012-01-01".format(self.url),
            "GET",
            headers=self.headers)

    def get_currency_rate(self, from_currency, to_currency, date):
        response, content = self.http.request(
            "{}currency/rate/{}/to/{}?date={}".format(self.url,
                                                      from_currency, to_currency,
                                                      date),
            "GET",
            headers=self.headers)
        return float(content)

    # get currency rates dictionary
    def get_currency_rates_dict(self, use_file):
        if self.currency_rates_dict is None:
            if use_file:
                # Get content of the file 'currency_rates_dict.json'
                file = open('../assets/currency_rates_dict.json', 'r')
                self.currency_rates_dict = loads(file.read())
                file.close()
            else:
                self.currency_rates_dict = {}
                date = '2012-01-01'
                currency = ['EUR', 'GBp', 'GBP', 'JPY', 'NOK', 'SEK', 'USD']
                for c1 in currency:
                    d = {}
                    for c2 in currency:
                        d[c2] = self.get_currency_rate(c1, c2, date)
                    self.currency_rates_dict[c1] = d
                print(dumps(self.currency_rates_dict))
        return self.currency_rates_dict

    def get_correlation_dict(self, asset_ids):
        if asset_ids is None:
            # get all assets
            response, content = self.get_all_assets()
            json_content = loads(content)
            asset_ids = []
            for asset_id in json_content:
                asset_ids.append(int(asset_id["ASSET_DATABASE_ID"]['value']))

        correlation_dict = {}
        ratio = [19]  # Correlation
        for asset_id in asset_ids:
            response, content = self.post_ratio_invoke(ratio, asset_ids, asset_id,
                                                       '2012-01-01', '2017-06-30')
            print(content)
            json_content = loads(content)
            # delete current asset from json
            del json_content[str(asset_id)]
            asset_correlations = {}
            for asset in json_content.items():
                asset_correlations[asset[0]] = string_result_to_float(asset[1]["19"]["value"])
            # TODO: To change add the list of sorted assets by correlation (reverse)
            # TODO: To change sorted(asset_correlations.items(), key=operator.itemgetter(1), reverse=True)
            correlation_dict[asset_id] = asset_correlations
        return correlation_dict

    def get_portfolio_sharpe(self):
        response, content = self.post_ratio_invoke([SHARPE], [PORTFOLIO_ID], None, '2012-01-01', '2017-06-30')
        return string_result_to_float(loads(content)[PORTFOLIO_ID][SHARPE]["value"])


client = Client()

def example_put_portfolio():
    body = {
        "label": "PORTFOLIO_USER3",
        "currency": {
            "code": "EUR"
        },
        "type": "front",
        "values": {
            "2012-01-01": [
                {
                    "asset": {
                        "asset": 405,
                        "quantity": 5
                    }
                },
                {
                    "asset": {
                        "asset": 67,
                        "quantity": 2
                    }
                }
            ]
        }
    }
    client.put_portfolio(body)
    response, content = client.get_portfolio()
    print(response)
    print(content)


def example_post_ratio_invoke():
    ratio = [17, 18, 20, 21],
    asset = [405, 61, 67, 16, 144, 70, 234, 376, 109, 31],
    start_date = "2012-01-01",
    end_date = "2017-06-30"
    response, content = client.post_ratio_invoke(ratio, asset, start_date, end_date)
    print(response)
    print(content)


def example_get_asset_quote():
    id = 405
    start_date = "2012-01-01"
    end_date = "2017-06-30"
    response, content = client.get_asset_quote(id, start_date, end_date)
    print(response)
    print(content)


def example_get_currency_rate():
    currency_from = 'USD'
    currency_to = 'EUR'
    print(client.get_currency_rate(currency_from, currency_to))


def example_get_correlation_dict():
    print(client.get_correlation_dict([405, 61, 67]))


def example_get_currency_rates_dict():
    print(client.get_currency_rates_dict())


def example_price_str_to_amount():
    print(client.price_str_to_amount('1,123871 USD', 'EUR'))


if __name__ == '__main__':
    kelly_is_testing = False
    if kelly_is_testing:
        # example_put_portfolio()
        # example_post_ratio_invoke()
        # example_get_asset_quote()
        # example_get_currency_rate()
        # example_get_correlation_dict()
        # client.put_portfolio(body)
        # example_get_currency_rates_dict()
        example_price_str_to_amount()
    else:
        client = Client()
        result = client.fill_all_assets()
        for a in result:
            print(a.toString())
        #response, ontent = client.get_all_caract()
        #a = loads(client.get_all_assets()[1])
        #b = loads(client.get_all_assets_infos()[1])
        #print(len(a))
        #print(len(b))

