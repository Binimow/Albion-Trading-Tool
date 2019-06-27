import itertools
import urllib.request as request
import json
from AllValuesAAPI import *
def reform_dict(x, y):
        current_item_id = x['item_id']
        current_city = CityList[y]
        sell_price = x['sell_price_min']
        return(current_item_id, current_city, sell_price)
def decode_url(url):
        with request.urlopen(url) as response:
            source = response.read()
            x = source.decode("utf-8")
            newstr = json.loads(x)
            return newstr
def process_info_api():
        x = ''
        #ItemLoop
        for i in ItemList.values():
                item = i
                y = 0
                ItemOrganised.update({item:[]})
                #CityLoop
                for x in CityList:
                        url = 'https://www.albion-online-data.com/api/v2/stats/prices/'+ str(item) + "?locations=" + x
                        decodedurl1 = decode_url(url)
                        refined1 = reform_dict(decodedurl1[0], y)
                        y += 1
                        ItemOrganised[item].append(refined1[2])  
        return(ItemOrganised)
def simple_best_offers(ItemOrganised):
        GoodItem = {}
        for itemName, itemValues in ItemOrganised.items():
                eachValue = list(itertools.permutations(itemValues, r=2))
                for i, j in eachValue:
                        if (j == 0):
                                continue
                        if (i/j) >= 1.5:
                                city1 = ItemOrganised[itemName].index(i)
                                city2 = ItemOrganised[itemName].index(j)
                                GoodItem[itemName] = i, city1, j, city2
        return(GoodItem)

def show_result(GoodItem):
        perf_city = []
        for i, j in GoodItem.items():
                a, b, c, d = j
                OrganisedCity[CityList[b]].append([i, a, c, CityList[d]])
                OrganisedCity[CityList[d]].append([i, c, a, CityList[b]])
                perf_city = (city_str(OrganisedCity, b))
        for i, j in perf_city.items():
                print('\n', i, ' :')
                for a, b, c, d in j:
                        print(a, ' :', b, '-->', c, ' :', d)
def city_str(OrganisedCity, current_city):
        current_str = []
        current_city = CityList[current_city]
        city_handling = []
        for j in OrganisedCity[current_city]:
                if len(j) != 0: 
                        current_stats = j[0], j[1], j[2], j[3]
                        current_str = current_stats
                else:
                        pass
        city_handling = [current_city, current_str[0], current_str[1], current_str[2], current_str[3]]
        yes_city = sort_list_city(city_handling)
        return(yes_city)

def sort_list_city(no_city):
        global yes_city
        i = no_city[4]
        if i not in yes_city.keys():
                yes_city[i] = []
                yes_city[i].append([no_city[1], no_city[3], no_city[0], no_city[2]])
        elif i in yes_city.keys():
                yes_city[i].append([no_city[1], no_city[3], no_city[0], no_city[2]])
        return(yes_city)
print('Processing..')        
show_result(simple_best_offers(process_info_api()))
input()
