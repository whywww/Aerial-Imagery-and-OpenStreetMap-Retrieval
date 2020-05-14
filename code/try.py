import requests
import matplotlib.pyplot as plt
import json


def download_aerial_img(latitide, longitude):

    zoom_level = 15

    params = {
        'key': 'AphqStoMZgeqc0JPIWYZHoYD2YZPIXNi2oQ6KoNbaWJhghGWlk5nFWcDQwuI-4yk',
        'centerPoint': f'{latitude}, {longitude}',
        'zl': f'{zoom_level}'
    }

    url = 'https://dev.virtualearth.net/REST/V1/Imagery/Metadata/Aerial/'
    r = requests.get(url, params=params)

    image_url = r.json()['resourceSets'][0]['resources'][0]['imageUrl']

    print(image_url)

    r = requests.get(image_url)

    with open('../images/picture.jpg', 'wb') as file:
        file.write(r.content)


if __name__ == '__main__':
    latitude, longitude = 42.057749, -87.675948
    download_aerial_img(latitude, longitude)