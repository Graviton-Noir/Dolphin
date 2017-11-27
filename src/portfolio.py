#!/usr/bin/env python

from quantity import compute_quantity_by_return
from asset import Asset, find_asset_with_id
from put_portfolio_default import Client as Dclient
from json import loads
from client import Client


class Portfolio:

    def __init__(self, max_money):
        self.items = []
        self.max_money = max_money
        self.client = Client()

    # Convert to json
    #  [
    #         {
    #            "asset": {
    #                "asset": 200,
    #                "quantity": 28.826869225
    #            }
    #        },
    #        {
    #            "asset": {
    #                "asset": 322,
    #                "quantity": 41.2371134021
    #            }
    #        }
    # ]
    def __str__(self):
        s = '['
        for item in self.items[:-1]:
            s += '{{ "asset": {{ "asset": {}, "quantity": {} }} }},'.format(item.asset.id, item.quantity)
        if len(self.items) > 0:
            s += '{{ "asset": {{ "asset": {}, "quantity": {} }} }}'.format(self.items[-1].asset.id,
                                                                                 self.items[-1].quantity)
        s += ']'
        return s

    # Build portfolio items from asset_ids
    def build_from_asset_ids(self, assets, asset_ids):
        if len(asset_ids) == 20:
            new_assets = []
            for id in asset_ids:
                for a in assets:
                    if a.id == id:
                        new_assets.append(a)
            self.build(new_assets)

    # Build portfolio items from assets list (20)
    def build(self, assets):
        for a in assets:
            self.items.append(PortfolioItem(a, compute_quantity_by_return(a)))

    # Build portfolio items from assets list (20)
    def build_with_sharpe_quantities(self, assets):
        if len(assets) == 20:
            percent_min = 0.01
            percent_max = 0.09
            weights = []

            sum_sharpes = sum(a.sharpe for a in assets)
            total_weights = 1
            # normalized sharpes
            for i in range(len(assets)):
                # Sharpe normalized between 0 and 0.80 (0.01 will be added later)
                w = assets[i].sharpe * 0.8 / sum_sharpes
                weights.append(percent_min + w)
                print('asset.sharpe: {}, total_weights: {}, w: {}'.format(assets[i].sharpe,
                                                                          total_weights, percent_min + w))
            # TODO: To remove. Sum weight to check that it's < 1.
            sum_weights = 0
            for w in weights:
                sum_weights += w
            print("sum(weights): {}".format(sum_weights))

            # Compute quantities from weights
            total = 0
            for i in range(len(assets)):
                # TODO: Check if the value is EUR.
                # Compute quantity
                quantity = round(((weights[i] * self.max_money) / assets[i].priceValue), 0)
                self.items.append(PortfolioItem(assets[i], quantity))
                total += quantity * assets[i].priceValue
            print("Total: {}".format(total))


    # Submit portfolio in server
    # PUT the given portfolio on the server and return information about it (sharpe)
    def submit(self):
        self.client.put_portfolio_from_assets(str(self))
        return self.client.get_portfolio_sharpe()

    #By Axel
    def get_ref_pf(self, assets):
        print (type(assets))
        print ("Initialising with the naif potfolio")
        client = Dclient()
        self.items= []
        reponse, content = client.get_portfolio(595)
        js = loads(content)
        for asset in js["values"]["2012-01-01"]:
            asset_id = asset["asset"]["asset"]
            asset_quantity = asset["asset"]["quantity"]
            self.items.append(PortfolioItem(
                find_asset_with_id(assets, asset_id),  asset_quantity))


class PortfolioItem:

    def __init__(self, asset, quantity):
        self.asset = asset
        self.quantity = quantity


if __name__ == '__main__':
    portfolio = Portfolio()
    #portfolio.get_ref_pf()
    portfolio.items.append(PortfolioItem(Asset(16, 1.409424248688, 1.409424248688, 4), 100))
    portfolio.items.append(PortfolioItem(Asset(61, 0.507142575734, 0.507142575734, 2), 101))
    print(portfolio)
