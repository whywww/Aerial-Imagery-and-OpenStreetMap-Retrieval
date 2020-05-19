import requests
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import shutil
import json


def get_my_map(mapArea, mapSize):
    if 'images' in os.listdir('../'):
        shutil.rmtree('../images')

    url = 'http://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial?'

    params = {
        'mapArea': f'{mapArea[0]},{mapArea[1]},{mapArea[2]},{mapArea[3]}',
        'mapSize': f'{mapSize[0]},{map_size[1]}',
        'key': 'AphqStoMZgeqc0JPIWYZHoYD2YZPIXNi2oQ6KoNbaWJhghGWlk5nFWcDQwuI-4yk',
    }

    r = requests.get(url, params=params)

    os.mkdir('../images')

    with open(f'../images/my_map.jpg', 'wb') as file:
        file.write(r.content)


def get_metadata(mapArea, mapSize):
    url = 'http://dev.virtualearth.net/REST/v1/Imagery/Map/Aerial?'

    params = {
        'mapArea': f'{mapArea[0]},{mapArea[1]},{mapArea[2]},{mapArea[3]}',
        'mapSize': f'{mapSize[0]},{map_size[1]}',
        'mmd': '1',
        'key': 'AphqStoMZgeqc0JPIWYZHoYD2YZPIXNi2oQ6KoNbaWJhghGWlk5nFWcDQwuI-4yk',
    }

    r = requests.get(url, params=params)

    bounding_box = r.json()['resourceSets'][0]['resources'][0]['bbox']
    map_center = r.json()['resourceSets'][0]['resources'][0]['mapCenter']['coordinates']

    return bounding_box, map_center


def process_my_map():
    pass


if __name__ == '__main__':
    # the area must have the format of [South Latitude, West Longitude, North Latitude, East Longitude]
    map_area = [42.053140, -87.676687, 42.060023, -87.672052]

    # width ranges between 80 and 2000, height ranges between 80 and 1500 (pixels)
    # if not set, default will be 350*350 pixel
    map_size = [2000, 1500]

    # get_my_map(map_area, map_size)
    bounding_box, center = get_metadata(map_area, map_size)

    # bounding box has the format of [South Latitude, West Longitude, North Latitude, East Longitude]


