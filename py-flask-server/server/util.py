import json
import pickle
import numpy as np


__locations = None
__data_columns = None
__model = None


def get_location_names():
    load_saved_artifacts()
    return __locations

def load_saved_artifacts():
    print("Artifacts being loaded..")
    global __data_columns
    global __locations

    with open("./artifacts/columns.json", 'r') as f:
         __data_columns = json.load(f)['data_columns']
         __locations = __data_columns[3:]
    global __model
    with open("./artifacts/texas_home_prices_model.pickle", 'rb') as f:
        __model = pickle.load(f)

    print("Artifacts loaded.")






def get_estimated_price(location, sqft, bed, bath):
    
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1
    
    x = np.zeros(len(__data_columns))
    x[0] = bed
    x[1] = sqft
    x[2] = bath
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)

if __name__ == '__main__':
    #load_saved_artifacts()
    print(get_location_names())
    #print(get_estimated_price('nevada', 1700, 3, 2))

    #print(get_estimated_price('morton', 1700, 3, 2))