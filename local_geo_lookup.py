import geocoder
from bs4 import BeautifulSoup
import requests
import pandas as pd

wiki_source = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M').text

wiki = BeautifulSoup(wiki_source, 'lxml')

wiki_table = wiki.find('table')

m_postal_codes = pd.read_html(str(wiki_table), header=0)[0]

#cleaning the codes marked as Not Assigned
toronto_pcodes = m_postal_codes[m_postal_codes['Borough'] != 'Not assigned']
toronto_pcodes = m_postal_codes[m_postal_codes['Neighbourhood'] != 'Not assigned']

#use a groupby to concatenate all the neighbourhood values to a single row
pcode_grouped = toronto_pcodes.groupby([toronto_pcodes['Postcode'], toronto_pcodes['Borough']])['Neighbourhood'].apply(', '.join).reset_index()
pcode_grouped.head()

#I found some stray brackets in the website data so I'm cleaning them here
pcode_grouped['Neighbourhood'].replace(to_replace=']', value='', regex=True, inplace=True)
pcode_grouped['Neighbourhood'].replace(to_replace='\[', value='', regex=True, inplace=True)

def gcoder_lookup (postcode):
    lat_lng_list = []
    for code in postcode:
        # initialize your variable to None
        lat_lng_coords = None

        # loop until you get the coordinates
        while(lat_lng_coords is None):
            g = geocoder.google('{}, Toronto, Ontario'.format(code))
            lat_lng_coords = g.latlng
        lat_lng_list.append(lat_lng_coords[1])
    return lat_lng_list

#test_list = [gcode_grouped['Neighbourhood']]

test_ll_list = gcoder_lookup(list(pcode_grouped['Postcode']))

print(test_ll_list)

#print(pcode_grouped.)
