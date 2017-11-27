#!/usr/bin/env python

from client import Client
from portfolio import PortfolioItem, Portfolio

class SebTestQuantitiesModel:

    def __init__(self):
        self.client = Client()

    # get assets with sharpe
    def select_assets(self, n_assets):
        assets = self.client.fill_all_assets()
        return sorted(assets, key=lambda a: a.sharpe, reverse=True)[:n_assets]

    # generate portfolio: assets with best sharpes
    def generate_portfolio(self, max_money, assets, n_assets):
        portfolio = Portfolio(max_money)
        # ta fonction est appelee dans portfolio.build
        portfolio.build(assets)
        return portfolio

    # Submit portfolio : PUT the given portfolio on the server and return information about it (sharpe)
    def submit_portfolio(self, portfolio):
        portfolio_str = str(portfolio)
        response, content = self.client.put_portfolio_from_assets(portfolio_str)
        print(response)
        print(content)
        return self.client.get_portfolio_sharpe()

    def run(self, n_assets, max_money):
        assets = self.select_assets(n_assets)
        portfolio = self.generate_portfolio(max_money, assets, n_assets)
        sharpe = model.submit_portfolio(portfolio)
        print(sharpe, str(portfolio))


if __name__ == '__main__':
    n_assets = 20
    max_money = 10000000
    model = SebTestQuantitiesModel()
    model.run(n_assets, max_money)

