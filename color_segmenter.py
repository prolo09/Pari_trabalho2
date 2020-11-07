#!/usr/bin/env python

import cv2
import argparse
import json
import numpy as np


def escolhamodo():
    # funcao para escolher os modos
    esc_modo = argparse.ArgumentParser(description="escolhe modo de canis")
    esc_modo.add_argument('-hsv', help="moda para o modo hvs", action="store_true")
    esc_modo.add_argument('--mostraCor', help="mostra a cor isolada", action="store_true")
    arg_list=vars(esc_modo.parse_args())
    return arg_list


def nothing(x):
    pass

def main():

    escolha=escolhamodo()


    windon_name='segmentacao'

    cap = cv2.VideoCapture(0)
    cv2.namedWindow(windon_name, cv2.WINDOW_AUTOSIZE)





    # criar as trackbar para escolha dos valores
    cv2.createTrackbar('min B/H', windon_name, 0, 255, nothing)
    cv2.createTrackbar('max B/H', windon_name, 0, 255, nothing)
    cv2.createTrackbar('min G/S', windon_name, 0, 255, nothing)
    cv2.createTrackbar('max G/S', windon_name, 0, 255, nothing)
    cv2.createTrackbar('min R/V', windon_name, 0, 255, nothing)
    cv2.createTrackbar('max R/V', windon_name, 0, 255, nothing)



    while True:

        _, frame = cap.read()

        #grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if escolha["hsv"]:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


        # vou buscar o valor defenidos nas trackbar
        minB_H=cv2.getTrackbarPos('min B/H', windon_name)
        maxB_H = cv2.getTrackbarPos('max B/H', windon_name)
        minG_S = cv2.getTrackbarPos('min G/S', windon_name)
        maxG_S = cv2.getTrackbarPos('max G/S', windon_name)
        minR_V = cv2.getTrackbarPos('min R/V', windon_name)
        maxR_V = cv2.getTrackbarPos('max R/V', windon_name)


        # cria matriz com os limites sinferior e superiors
        lim_inf= np.array([minB_H,minG_S,minR_V])
        lim_sup=np.array([maxB_H,maxG_S,maxR_V])


        # aplica um treshold com esse limites
        mask=cv2.inRange(frame, lim_inf, lim_sup)

        if escolha["mostraCor"]:
            # caso quera imprimir nao mostrando a cor mesmo real

            frame_com_cor = cv2.bitwise_and(frame, frame, mask=mask)
            cv2.imshow('jdj', mask)
            cv2.imshow(windon_name, frame_com_cor)
        else:
            # para imprimir caso queira isolar a cor e mostrando
            cv2.imshow(windon_name, mask)


        key=cv2.waitKey(1)
        if key==113:
            break
        elif key==119:
            dic_limite = dict(G={'max': maxG_S, 'min': minG_S},
                              R={'max': maxR_V, 'min': minR_V},
                              B={'max': maxB_H, 'min': minB_H})

            file_name = 'limits.json'
            with open(file_name, 'w') as file_handle:
                print('writing dictionary Limites to file ' + file_name)
                json.dump(dic_limite, file_handle)
            break









if __name__ == '__main__':
    main()



