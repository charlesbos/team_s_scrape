"""
sainsburys.py

This modules extracts prices and item titles from a valid Sainsburys store page
url and then returns that data.

Created by: Charles Bos
Contributors: Charles Bos
"""

from operator import itemgetter
from fetcher import htmlFetch

def sainsburysData(url) :
    '''
    Extract Sainsburys prices and item titles
    One argument accepted, a url which can be passed to the htmlFetch function
    from the fetcher module.
    '''

    htmlString = htmlFetch(url)
    
    # Extract prices
    priceStart = htmlString.find('<p class="pricePerUnit">') + 24

    if priceStart == -1 :
        print("No prices here. Sorry.")
    else :
        priceEnd = priceStart + 8
        priceExtract = htmlString[priceStart + 2:priceEnd - 1]
        priceList = [priceExtract]
        
        while priceStart != 23 :
            priceStart = htmlString.find('<p class="pricePerUnit">', priceEnd) + 24
            priceEnd = priceStart + 8
            priceExtract = htmlString[priceStart + 2:priceEnd - 1]
            priceList.extend([priceExtract])

        priceList = priceList[:-1]

    # Extract titles
    titleStart = htmlString.find('''<a href="http://www.sainsburys.co.uk/shop/gb/groceries/still-water/''') + 67

    if titleStart == -1 :
        print("No titles here. Sorry.")
    else :
        titleEnd = htmlString.find('<img alt=', titleStart) + 9
        titleExtract = htmlString[titleStart:titleEnd].partition(' ')[-1].partition('\r\n')[0].strip(' ')
        titleList = [titleExtract]

        while titleStart != 75 :
            titleStart = htmlString.find('''<a href="http://www.sainsburys.co.uk/shop/gb/groceries/still-water/''', titleEnd) + 76
            titleEnd = htmlString.find('<img alt=', titleStart) + 9
            titleExtract = htmlString[titleStart:titleEnd].partition(' ')[-1].partition('\r\n')[0].strip(' ')
            titleList.extend([titleExtract])

        titleList = titleList[:-1] 

    # Extract promotion titles
    proTitleStart = htmlString.find('''<a href="http://www.sainsburys.co.uk/shop/ProductDisplay?''') + 57

    if proTitleStart == -1 :
        print("No titles here. Sorry.")
    else:
        proTitleEnd = htmlString.find('<img alt=', proTitleStart) + 9
        proTitleExtract = htmlString[proTitleStart:proTitleEnd].partition(' ')[-1].partition('\r\n')[0].strip(' ')
        proTitleList = [proTitleExtract]

        while proTitleStart != 65 :
            proTitleStart = htmlString.find('''<a href="http://www.sainsburys.co.uk/shop/ProductDisplay?''', proTitleEnd) + 66
            proTitleEnd = htmlString.find('<img alt=', proTitleStart) + 9
            proTitleExtract = htmlString[proTitleStart:proTitleEnd].partition(' ')[-1].partition('\r\n')[0].strip(' ')
            proTitleList.extend([proTitleExtract])

        proTitleList = proTitleList[:-1]

    # Merge the lists
    try :
        titleList = titleList + proTitleList
        titleList = sorted(titleList)
    except NameError :
        pass

    # Turn the two lists into a dictionary and return it
    if len(priceList) != len(titleList) :
        print("Error. Lengths of prices and item titles do not match.")
    else :
        pricesComparison = dict(zip(titleList, priceList))
        return sorted(pricesComparison.items(), key=itemgetter(1))


                            


                    


