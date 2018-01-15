from googleplaces import GooglePlaces, types, lang
from collections import Counter
import time
import random
import pandas
import unicodedata
import datetime
import config
#1000 meters

radius = config.RADIUS

# Google Keys
new_keys = list(pandas.read_csv(config.INPUT_KEYS_LIST).iloc[:,0])
len(new_keys)


def get_place_details(place_id, key):

    place = None
    google_places = GooglePlaces(key)

    while (place is None):
        try:
            place = google_places.get_place(place_id)

        except Exception as e:

            # check for NOT FOUND error (place not found)
            if 'NOT_FOUND' in e.message:
                print 'Place not found error - ' + place_id
                return None # return back to caller
            else:
                print 'sleeping for ' + place_id + ' using key: ' + key + " : " + str(e.message)
                time.sleep(3)
                place = None
                key = random.choice(new_keys)
                google_places = GooglePlaces(key)

    return place

if __name__ == '__main__':



    set_outputs = list(pandas.read_csv(config.INPUT_SEARCH_PLACE_IDS).iloc[:,1])

    ##############################################################################
    '''
        [Step 2] - Get Place details per Place ID
    '''
    ##############################################################################

    place_details = []


    for i, id in enumerate(set_outputs[config.INDEX_START:len(set_outputs)]):
        key = new_keys[i%len(new_keys)]
        #print(str(i%len(new_keys)))
        place = get_place_details(id, key)

        if place is not None:
            type = str(place.types).encode('unicode-escape')
            name = place.name.encode('unicode-escape')
            lat =  place.geo_location['lat']
            lng =  place.geo_location['lng']
            vicinity = place.vicinity.encode('unicode-escape')
            id = place.place_id

            print(str([name, type, lat, lng, vicinity, id]))

            place_details.append([name, type, lat, lng, vicinity, id])

        if len(place_details) == 2000:
            print()
            print('Saving 2000 places to csv file')
            print(str(datetime.datetime.now()))
            print()
            print()

            with open(config.OUTPUT_FILE, 'a') as f:
                pandas.DataFrame(place_details).to_csv(f, header=False)
            place_details = []
    #pandas.DataFrame(place_details, columns = ['name', 'type','lat','lng','vicinity','id']).to_csv('output_places.csv', index=False)

    if len(place_details) > 0:
        with open(config.OUTPUT_FILE, 'a') as f:
            pandas.DataFrame(place_details).to_csv(f, header=False)