#Recuit simule.py

#OCD > Coding style
from client     import Client
from asset      import Asset
from portfolio  import Portfolio, PortfolioItem
from util       import compute_item_NAV
from quantity   import compute_quantity_by_return
import random
from subprocess import Popen
from parse      import *


#By Axel, powered by franglais
if __name__ == '__main__':
    #Getting all assest
    c = Client()
    all_assets = c.fill_all_assets()

    #Chargement du portefeuille naif
    portefeuille = Portfolio()
    portefeuille.get_ref_pf(all_assets)

    #Getting original sharpe value
    tester = Popen('/bin/sh', '-c', 'java -jar ../crack/EvaluationSolo.jar',
                stdout=PIPE)
    parsed = parse('PORTFOLIO_USER3 / Sharpe : {f} / Note : {d}/20)', line)
    sharpe = 0
    if parsed != None:
        sharpe = parsed['f']

    locked_up = 0
    #lancement du recuit simule
    while locked_up < 100:
        #Election du nouvel asset
        old_asset_index = random.randint(0, 20)
        new_asset_index = random.randint(0, len(all_assets))
        tmp = portefeuille.items[old_asset_index]
        quantity = -42 #Will be fixed by compute function
        portefeuille.items[old_asset_index] = PortfolioItem(
                all_assets[new_asset_index], quantity)
        compute_quantity_by_return(portefeuille.items[old_asset_index])

        #Checking the NAV:  1% < NAV < 10%
        nav = compute_item_NAV(portefeuille[old_asset_index], portefeuille)
        while nav < 1 or nav > 10:
            new_asset_index = random.randint(0, len(all_assets))
            quantity = 2
            portefeuille.items[old_asset_index] = PortfolioItem(
                all_assets[new_asset_index], quantity)
            nav = compute_item_NAV(portefeuille[old_asset_index], portefeuille)

        #TODO Push here the portefeuille to the server for evaluation

        #Launching the testing program, and parsing the result
        tester = Popen('/bin/sh', '-c', 'java -jar ../crack/EvaluationSolo.jar',
                stdout=PIPE)
        classe = True
        valide = True
        found = False
        new_sharpe = 0
        note = 0
        #Parse each line, check si c'est valide, ou class'e et get le sharpe
        for line in tester.stdout:
            parsed = parse('***Hors classement mais valide (note = 10/20)***'
                    ,line)
            if parsed != None and not found:
                classe = False
            parsed = parse('***Hors classement et ne sont pas valide (note = 0/20)***'
                    ,line)
            if parsed != None and not found:
                valide = False
            parsed = parse('PORTFOLIO_USER3 / Sharpe : {f} / Note : {d}/20)', line)
            if parsed != None:
                note = parsed['d']
                new_sharpe = parsed['f']
                found = True
        print "Sharpe: " + str(new_sharpe) +" Note: " + str(note) + " Valide: " + str(valide)

        #check if we keep it
        if new_sharpe < old_sharpe:
            portefeuille.items[old_asset_index] = tmp
            locked_up = locked_up + 1
        else:
            locked_up = 0

    #End of recuit simule
    #Maybe print the result ?




