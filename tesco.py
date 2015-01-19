"""
tesco.py

This modules extracts prices and item titles from a valid Tesco store page
url and then returns that data.
"""
from fetcher import simpleFetch

def tescoData(url, titletag, unit, scroll) :
    '''
    Extract Tesco prices per measure and item titles.
    Three arguments are accepted. The first is a url which can be passed to the htmlFetch function.
    The second is a unit to append to the extracted prices.
    from the fetcher module. The third and fourth are not used in this function
    at all and are specified for compatibility reasons only.
    '''

    htmlString = simpleFetch(url)

    if htmlString == 'null' :
        print("TescoError: failed to retrieve webpage.")
        return 'null'
    else :
        # Extract prices
        priceList = []
        priceStart = htmlString.find('<span class="linePriceAbbr">')
        priceEnd = htmlString.find('/', priceStart)
        
        while (0 <= priceStart <= len(htmlString)) is True :
            priceExtract = htmlString[priceStart + 28:priceEnd].strip('()') + unit
            measureCheck = htmlString[priceEnd:priceEnd + 5]
            if measureCheck == '/75cl' :
                temp = str('{:.2f}'.format(((float(htmlString[priceStart + 28:priceEnd].strip('()')[1:]) / 30) * 4)))
                priceExtract = '£' + temp + unit
            if (measureCheck == '/l)</') or (measureCheck == '/kg)<') :
                temp = str('{:.2f}'.format((float(htmlString[priceStart + 28:priceEnd].strip('()')[1:]) / 10)))
                priceExtract = '£' + temp + unit
            priceList += [priceExtract]
            priceStart = htmlString.find('<span class="linePriceAbbr">', priceEnd)
            priceEnd = htmlString.find('/', priceStart)

        # Extract titles
        titleList = []
        titleStart = htmlString.find('<span data-title="true">') + 24
        titleEnd = htmlString.find('</span>')

        while (0 <= titleStart <= len(htmlString)) is True :
            titleExtract = htmlString[titleStart + 24:titleEnd].partition('&gt;')[0]
            itemExistCheck = htmlString.find('Sorry, this product is currently not available.', titleEnd, titleEnd + 200)
            if itemExistCheck == -1 :
                titleList.extend([titleExtract])
            titleStart = htmlString.find('<span data-title="true">', titleEnd)
            titleEnd = htmlString.find('</span></a></h2>', titleStart)

        titleList = [x for x in titleList if x != '']

        # Merge the two lists into one list of tuples and return it
        if len(priceList) != len(titleList) :
            print("TescoError: lengths of prices and item titles do not match.")
            return 'null'
        else :
            return [list(x) for x in zip(titleList, priceList, ["Tesco"] * len(priceStart))]


                            


                    


