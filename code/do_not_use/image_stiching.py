import cv2
import numpy as np
import matplotlib.pyplot as plt


def make_a_map(path):
    result = None
    # use these index to load images
    lat = 0
    long = 1

    while True:
        long = 1
        long_img = cv2.imread(f'{path}/img_{lat}_{0}.jpg')
        while True:

            img = cv2.imread(f'{path}/img_{lat}_{long}.jpg')
            if img is None:
                break
            long_img = np.concatenate((long_img, img), axis=1)
            long += 1

        if long_img is None:
            break

        # plt.imshow(long_img)
        # plt.show()

        lat += 1
        if result is None:
            result = long_img
        else:
            result = np.concatenate((result, long_img), axis=0)

    cv2.imwrite('../result/result.png', result)


# def stich_horizontal(img1, img2):
#     return np.concatenate((img1, img2), axis=1)


if __name__ == '__main__':
    path = '../images/'
    make_a_map(path)
