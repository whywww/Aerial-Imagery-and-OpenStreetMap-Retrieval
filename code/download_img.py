import requests
import numpy as np
import shutil
import os
from tqdm import tqdm
import threading
import time

start = time.perf_counter()


def download_aerial_img(latitude, longitude, filename):
    """
    Download 1 aerial image at given location and save it in 'images' folder.

    :param latitude:
    :param longitude:
    :param filename:
    :return: Nothing
    """
    
    zoom_level = 20
    params = {
        'key': 'AphqStoMZgeqc0JPIWYZHoYD2YZPIXNi2oQ6KoNbaWJhghGWlk5nFWcDQwuI-4yk',
        'centerPoint': f'{latitude}, {longitude}',
        'zl': f'{zoom_level}'
    }

    url = 'https://dev.virtualearth.net/REST/V1/Imagery/Metadata/Aerial/'
    r = requests.get(url, params=params)

    image_url = r.json()['resourceSets'][0]['resources'][0]['imageUrl']

    r = requests.get(image_url)

    with open(f'../images/{filename}.jpg', 'wb') as file:
        file.write(r.content)


def get_aerial_img(bounding_box):
    """
    :param bounding_box: a list [min_lat, max_lat, min_lon, max_lon] containing the boundary of the images.
    :return: Nothing
    """
    if 'images' in os.listdir('../'):
        shutil.rmtree('../images')
    min_lat, max_lat, min_lon, max_lon = bounding_box[0], bounding_box[1], bounding_box[2], bounding_box[3]
    sample_interval = 0.0004

    num_lat = int((max_lat - min_lat) / sample_interval)
    num_long = int((max_lon - min_lon) / sample_interval)

    latitudes = np.linspace(start=min_lat, stop=max_lat, num=num_lat)
    longitudes = np.linspace(start=min_lon, stop=max_lon, num=num_long)

    # interval = latitudes[1] - latitudes[0]
    # print(interval)

    # print(f'latitudes is {latitudes}')
    # print(f'longitudes is {longitudes}')

    os.mkdir('../images')
    threads = []

    for idx_lat, latitude in enumerate(latitudes):
        time.sleep(1)
        for idx_long, longitude in enumerate(longitudes):

            filename = f'img_{idx_lat}_{idx_long}'
            t = threading.Thread(target=download_aerial_img, args=[latitude, longitude, filename])
            t.start()
            threads.append(t)

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    boundary = [42.048957, 42.063487, -87.680418, -87.669603, ]

    get_aerial_img(boundary)

    finish = time.perf_counter()

    print(f'Finished in {round(finish - start, 2)} second(s)')
