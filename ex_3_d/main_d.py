#! /usr/bin/python
import partial_def as pd
import cv2
import json
from functools import partial


def main():

    Limites = {'B' : {'max' : 200, 'min' : 100},
               'G' : {'max' : 200, 'min' : 100},
               'R' : {'max' : 200, 'min' : 100}}

    window_name = 'segmentacao'
    image_path = "/home/alex/PycharmProjects/PARI/Parte05/images/atlascar.png"
    img = cv2.imread(image_path, 1)
    cv2.namedWindow(window_name)


    Bmin = partial(pd.TB_Bmin, ImageBGR=img, window=window_name, limits=Limites)
    Bmax = partial(pd.TB_Bmax, ImageBGR=img, window=window_name,limits=Limites)
    Gmin = partial(pd.TB_Gmin, ImageBGR=img, window=window_name,limits=Limites)
    Gmax = partial(pd.TB_Gmax, ImageBGR=img, window=window_name,limits=Limites)
    Rmin = partial(pd.TB_Rmin, ImageBGR=img, window=window_name,limits=Limites)
    Rmax = partial(pd.TB_Rmax, ImageBGR=img, window=window_name,limits=Limites)


    cv2.createTrackbar('Min B', window_name, 128, 255, Bmin)
    cv2.createTrackbar('Max B', window_name, 128, 255, Bmax)
    cv2.createTrackbar('Min G', window_name, 128, 255, Gmin)
    cv2.createTrackbar('Max G', window_name, 128, 255, Gmax)
    cv2.createTrackbar('Min R', window_name, 128, 255, Rmin)
    cv2.createTrackbar('Max R', window_name, 128, 255, Rmax)

    cv2.imshow(window_name,img)
    cv2.waitKey(0)

    file_name = 'limits.json'
    with open(file_name, 'w') as file_handle:
        print('writing dictionary Limites to file ' + file_name)
        json.dump(Limites, file_handle)  #Limits is a dictionary


if __name__ == '__main__':
    main()