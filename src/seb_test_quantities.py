#!/usr/bin/env python

from client import Client
from portfolio import PortfolioItem, Portfolio

class SebTestQuantitiesModel:

    def __init__(self):
        self.client = Client()

    # get assets with sharpe
    def select_assets(self, n_assets):
        assets, assets_dict = self.client.fill_all_assets_split()
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


    sum = 1143111.3370617537 \
          + 201799.65011187998 \
          + 41983.82537747577 \
          + 506678.801693727 \
          + 252563.14312428157 \
          + 337933.37865401985 \
          + 996871.521969843 \
          + 2204569.0679060477 \
          + 26225.363070545176 \
          + 119063.47694812567 \
          + 24040.58460676713 \
          + 94734.48510646823 \
          + 210655.7377049266 \
          + 1645040.5128143644 \
          + 124666.44253315279 \
          + 277361.38836112 \
          + 165848.97338770135 \
          + 347595.8338989143 \
          + 347575.2072832628 \
          + 186744.84719262682
    print(sum)

    n_assets = 20
    max_money = 10000000
    model = SebTestQuantitiesModel()
    model.run(n_assets, max_money)

