import pickle
import json
import zipfile

import numpy as np

__weathers = None
__data_columns = None
__model = None


def get_predicted_visibility(temp, hum, ws, wb, pressure, month, weather):
    global __data_columns
    global __model

    try:
        loc_index = __data_columns.index(weather)
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0], x[1], x[2], x[3], x[4], x[5] = temp, hum, ws, wb, pressure, month

    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns
    global __weathers
    global __model

    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __weathers = __data_columns[6:]  # first 6 are 'temperature','humidity',
        #  'wind_speed','wind_bearing','pressure','month'
        print("columns loaded")

    if __model is None:
        with zipfile.ZipFile("./artifacts/model_rf.pkl.zip", 'r') as file:
            file.extractall()

        with open('model_rf.pkl', 'rb') as f:  # rb as its a binary file
            __model = pickle.load(f)
            print("model loaded")

    print("loading saved artifacts...done")


def get_weathers():
    return __weathers


def get_data_columns():
    return __data_columns


if __name__ == "__main__":
    load_saved_artifacts()