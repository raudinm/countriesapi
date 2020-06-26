import json, requests

API_KEY = '26a384ee292eed7b8802b0b56cb72efd'

def sendRequest(url):
    response = requests.get(url)
    data = response.json()

    try:
        error = data.get('error', None)
    except AttributeError as e:
        error = None
    
    if error != None:
        print(error)
        return
    return data

def getRegions(alpha2code, api_key=API_KEY):
    url = 'http://battuta.medunes.net/api/region/{countryCode}/all/?key={key}'\
            .format(key=api_key, countryCode=alpha2code)
    return sendRequest(url)

def getCitiesByRegion(alpha2code, region, api_key=API_KEY):
    url = 'http://battuta.medunes.net/api/city/{countryCode}/search/?region={region}&key={key}'\
            .format(countryCode=alpha2code, region=region, key=api_key)
    return sendRequest(url)
        
def saveRegionsToFile():
    with open('countries.json', 'r') as countries:
        temp_data = json.load(countries)
        
        index = 0
        while index < len(temp_data):
            print('Procesando...')
            print(temp_data[index]['name'])
            print('\n')
            
            status = temp_data[index].get('states', None)
            if status == None:
                states = getRegions(temp_data[index]['alpha2Code'])

                if states != None:
                    print('Agregando regiones del pais {country}...'.format(country=temp_data[index]['name']))
                    print('\n')
                    
                    temp_data[index]["states"] = states
                else:
                    return
            else:
                print('Omitiendo... {country}'.format(country=temp_data[index]['name']))
                index += 1
                continue
            index += 1
        
        with open('countries_regions1.json', 'w') as file:
            json.dump(temp_data, file, indent=4)

def saveCitiesToFile():
    with open('countries_regions_cities.json', 'r') as countries:
        temp_data = json.load(countries)

        index = 0
        while index < len(temp_data):
            if len(temp_data[index]['states']) > 0:
                
                index2 = 0
                while index2 < len(temp_data[index]['states']):
                    country_code = temp_data[index]['states'][index2]['country']
                    region = temp_data[index]['states'][index2]['region']
                    
                    if len(region) < 3: # una region no puede tener menos de 3 caracteres para la api
                        index2 += 1
                        continue

                    status = temp_data[index]['states'][index2].get('cities', None)
                    if status == None:
                        cities = getCitiesByRegion(alpha2code=country_code, region=region)

                        if cities != None:
                            print('Agregando ciudades a la region {region}...'.format(region=temp_data[index]['states'][index2]['region']))
                            print('Pais de origen {country}...'.format(country=temp_data[index]['name']))
                            print('\n')
                            temp_data[index]['states'][index2]['cities'] = cities
                        else:
                            with open('countries_regions_cities.json', 'w') as file:
                                json.dump(temp_data, file, indent=4) 
                            return
                    else:
                        print('Omitiendo region... {region}'.format(region=temp_data[index]['states'][index2]['region']))
                        index2 += 1
                        continue

                    index2 += 1
            index += 1

        with open('countries_regions_cities.json', 'w') as file:
            json.dump(temp_data, file, indent=4)            
        
if __name__ == "__main__":
    saveCitiesToFile()


# with open('states.json', 'r') as states:
#     st_data = json.load(states)
    
#     with open('states_and_cities.json', 'r') as cities:
#         ct_data = json.load(cities)

#         lista = []
#         for ct in ct_data:
#             value = filter(lambda x: x['name'] == ct, st_data)
#             if(len(value) > 0):
#                 value[0]['cities'] = ct_data[ct]
#                 lista.append(value[0])

#         with open('usa.json', 'w') as file:
#             json.dump(lista, file, indent=4)