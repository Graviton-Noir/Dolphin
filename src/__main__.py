#!/usr/bin/env python

from asset_2 import Assett
from basic_model_2 import BasicModel
from evaluate import check_portfolio
from client import Client

if __name__ == '__main__':
    n_assets = 20
    max_money = 10000000
    # TODO: To uncomment: c = Client()
    # TODO: To uncomment: assets = c.fill_all_assets()
    assets = [Assett(16, 1.409424248688, 1.409424248688),
              Assett(31, 0.751849284981, 0.751849284981),
              Assett(61, 0.507142575734, 0.507142575734),
              Assett(70, 1.07826992451, 1.07826992451),
              Assett(109, 0.092134124, 0.0002134124)]

    model = BasicModel()
    portfolio = model.generate_portfolio(max_money, assets, n_assets)
    check_portfolio(portfolio)
    client = Client()
    response, content = client.put_portfolio_from_assets(str(portfolio))
    print(response)
    print(content)
