#!/usr/bin/env python3

from asset import Asset
from quantity import compute_quantity_by_return

class Portfolio:

    def __init__(self, max_money):
        self.items = []
        self.max_money = max_money

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


class PortfolioItem:

    def __init__(self, asset, quantity):
        self.asset = asset
        self.quantity = quantity
