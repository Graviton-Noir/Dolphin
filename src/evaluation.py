#!/usr/bin/env python

from portfolio import Portfolio
from util import list_to_str, is_in_list
from data_manager import DataManager

MAX_MONEY = 10000000


class Evaluation:

    def __init__(self):
        self.best_portfolio = None
        self.best_sharpe = None
        self.out_file = open('../out/trees/1', 'w')
        self.dm = DataManager()
        # list of combinations already evaluated. each of them are ordered
        # ex: BACD -> [order] -> ABCD -> [is in list?] -> already evaluated or not.
        self.combinations = []

    def __exit__(self):
        self.out_file.close()

    # Evaluate combination
    def evaluate(self, ids_combination):
        ids_combination = sorted(ids_combination)
        # check if already evaluated
        if not is_in_list(ids_combination, self.combinations):
            # Get assets array from ids array
            assets_combination = self.ids_to_assets_array(ids_combination)
            # Generate portfolio from given assets_combination
            portfolio = Portfolio(MAX_MONEY)
            portfolio.build(assets_combination)
            portfolio_sharpe = portfolio.submit()
            # save if better
            if portfolio_sharpe > self.best_sharpe:
                self.best_sharpe = portfolio_sharpe
                self.best_portfolio = portfolio
            s = '{{ "sharpe": {}, "portfolio": {} }}'.format(portfolio_sharpe, str(portfolio))
            print(s)
            self.out_file.write('{}\n'.format(s))            # add in combinations list after evaluation
            self.combinations.append(ids_combination)
        print('evaluate_combination: {}'.format(ids_combination))

    # Evaluate combination and compute quantities according to the sharpe.
    # Higher the sharpe is, higher the %nav will be
    def evaluate_with_sharpe_quantities(self, ids_combination):
        ids_combination = sorted(ids_combination)
        # check if already evaluated
        if not is_in_list(ids_combination, self.combinations):
            # Get assets array from ids array
            assets_combination = self.ids_to_assets_array(ids_combination)
            # Generate portfolio from given assets_combination
            portfolio = Portfolio(MAX_MONEY)
            portfolio.build_with_sharpe_quantities(assets_combination)
            portfolio_sharpe = portfolio.submit()
            # save if better
            if portfolio_sharpe > self.best_sharpe:
                self.best_sharpe = portfolio_sharpe
                self.best_portfolio = portfolio
            s = '{{ "sharpe": {}, "portfolio": {} }}'.format(portfolio_sharpe, str(portfolio))
            print(s)
            self.out_file.write('{}\n'.format(s))  # add in combinations list after evaluation
            self.combinations.append(ids_combination)
        print('evaluate_combination: {}'.format(ids_combination))

    # Get assets array from ids array
    def ids_to_assets_array(self, assets_ids):
        assets_dict = self.dm.get_assets_dict()
        assets_from_ids = []
        # build assets array from ids
        for id in assets_ids:
            assets_from_ids.append(assets_dict[str(id)])
        return assets_from_ids