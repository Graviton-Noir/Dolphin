#!/usr/bin/env python

from client import Client
import random
from portfolio import PortfolioItem, Portfolio


class RandomModel:
    # get random assets
    @staticmethod
    def select_assets(assets, n_assets):
        return random.sample(assets, n_assets)

    # generate portfolio with random assets and quantity
    def generate_portfolio(self, max_money, assets, n_assets):
        percent_min = 0.01 * (20 / n_assets)
        percent_max = 0.09 * (20 / n_assets)
        best_assets = self.select_assets(assets, n_assets)
        portfolio = Portfolio()
        weights = []
        total_weights = 1 - n_assets * percent_min
        # Generate random weights between 1% and 10%
        for i in range(len(best_assets)):
            w = 0
            if total_weights > 0:
                w = random.uniform(0, percent_max if total_weights > percent_max else total_weights)
                print('total_weights: {}, w: {}'.format(total_weights, w))
            weights.append(percent_min + w)
            total_weights -= w

        # TODO: To remove. Sum weight to check that it's < 1.
        sum_weights = 0
        for w in weights:
            sum_weights += w
        print("sum(weights): {}", sum_weights)

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
    model = RandomModel()
    portfolio = model.generate_portfolio(max_money, assets, n_assets)
    print(portfolio)
