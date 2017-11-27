#!/usr/bin/env python3

from portfolio import PortfolioItem


# replace , by . and convert to float
def string_result_to_float(s):
    return float(s.replace(',', '.'))


# PTF of a portFolioItem
# Used in NAv computation
def compute_item_PTF(portFolioItem):
    return portFolioItem.quantity * portFolioItem.asset.monetaryNumber.amount


# PTF of portfolio
def compute_portfolio_PTF(portFolio):
    ptfSum = 0
    for item in portFolio.items:
        ptfSum += compute_item_PTF(item)
    return ptfSum


# NAV computation
def compute_item_NAV(portFolioItem, portFolio):
    return compute_item_PTF(portFolioItem) / compute_portfolio_PTF(portFolio)


def list_to_str(list):
    s = ''
    for l in list[:-1]:
        s += '{}, '.format(str(l))
    if len(list) > 0:
        s += str(list[-1])
    return s
