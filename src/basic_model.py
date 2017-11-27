#!/usr/bin/env python

from client import Client
from asset import Assett
import random
from portfolio import PortfolioItem, Portfolio

# model where the assets with best sharpes are selected
# the weights are according sharpes
class BasicModel:

    # get assets with sharpe
    @staticmethod
    def select_assets(assets, n_assets):
        return sorted(assets, key=lambda a: a.sharpe, reverse=True)[:n_assets]

    # generate portfolio: assets with best sharpes
    def generate_portfolio(self, max_money, assets, n_assets):
        best_assets = self.select_assets(assets, 5)
        percent_min = 0.01
        percent_max = 0.09
        portfolio = Portfolio()
        weights = []

        sum_sharpes = sum(a.sharpe for a in best_assets)
        total_weights = 1
        # normalized sharpes
        for i in range(len(best_assets)):
            # Sharpe normalized between 0 and 0.80 (0.01 will be added later)
            w = best_assets[i].sharpe * 0.8 / sum_sharpes
            weights.append(percent_min + w)
            print('asset.sharpe: {}, total_weights: {}, w: {}'.format(best_assets[i].sharpe,
                                                                      total_weights, percent_min + w))
        # TODO: To remove. Sum weight to check that it's < 1.
        sum_weights = 0
        for w in weights:
            sum_weights += w
        print("sum(weights): {}".format(sum_weights))

        # Compute quantities from weights
        total = 0
        for i in range(len(best_assets)):
            # TODO: Check if the value is EUR.
            # Compute quantity
            quantity = round(((weights[i] * max_money) / best_assets[i].priceValue), 0)
            portfolio.items.append(PortfolioItem(best_assets[i], quantity))
            total += quantity * best_assets[i].priceValue
        print("Total: {}".format(total))
        return portfolio


if __name__ == '__main__':
    n_assets = 20
    max_money = 10000000
    c = Client()
    assets = c.fill_all_assets()
    model = BasicModel()
    portfolio = model.generate_portfolio(max_money, assets, n_assets)
    check
    print(portfolio)
