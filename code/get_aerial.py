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

    with open(f'../images/my_map_unprocessed.jpg', 'wb') as file:
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


def process_my_map(bounding_box, map_area):
    my_map = cv2.imread('../images/my_map_unprocessed.jpg')
    if my_map is None:
        print('No map loaded!')
        return

    height, width = my_map.shape[0], my_map.shape[1]
    print(bounding_box)
    print(map_area)

    lat_step = (bounding_box[2] - bounding_box[0]) / height
    long_step = (bounding_box[3] - bounding_box[1]) / width
    top, left, bottom, right = 0, 0, 0, 0

    print(lat_step)
    print(long_step)

    for i in range(height):
        current_lat = bounding_box[0] + i*lat_step  # adding from the south to north
        if current_lat > map_area[2]:
            bottom = i
            break

    for i in range(height):
        current_lat = bounding_box[0] + i*lat_step  # adding from the south to north
        if current_lat > map_area[0]:
            top = i
            break

    for i in range(width):
        current_long = bounding_box[1] + i*long_step  # adding from the east to west
        if current_long > map_area[3]:
            right = i
            break

    for i in range(width):
        current_long = bounding_box[1] + i*long_step  # adding from the east to west
        if current_long > map_area[1]:
            left = i
            break

    my_map = my_map[top:bottom, left:right]

    cv2.imwrite('../images/my_map.png', my_map)


if __name__ == '__main__':
    # the area must have the format of [South Latitude, West Longitude, North Latitude, East Longitude]
    map_area = [42.050993, -87.679421, 42.061049, -87.670194]

    # width ranges between 80 and 2000, height ranges between 80 and 1500 (pixels)
    # if not set, default will be 350*350 pixel
    map_size = [2000, 1500]

    get_my_map(map_area, map_size)
    bounding_box, center = get_metadata(map_area, map_size)
    # bounding box has the format of [South Latitude, West Longitude, North Latitude, East Longitude]
    process_my_map(bounding_box, map_area)
