#!/usr/bin/env python

import argparse
import readchar
import cv2
import json
import numpy as np

# variaveis globais
ponto_ini = [0, 0]
tela = np.ones([500, 500, 3], 'uint8') * 255


def escolhamodo():
    parser = argparse.ArgumentParser(description="PARI AR Paint")
    parser.add_argument('-js',
                        '--json',
                        help="Full path to json file",
                        action="store_true")
    parser.add_argument('-info',
                        '--more_info',
                        help="List of commands",
                        action="store_true")
    args = vars(parser.parse_args())
    return args


def instrucoes():
    # Command list
    print('''
    !! PARI AR PAINT !!
    Here are some commands u can use:
    - RED PAINT     -> PRESS 'r'
    - GREEN PAINT   -> PRESS 'g'
    - BLUE PAINT    -> PRESS 'b'
    - THICKER BRUSH -> PRESS '+'
    - THINNER BRUSH -> PRESS '-'
    - SAVE          -> PRESS 'w'
    - CLEAR         -> PRESS 'c'
    - QUIT          -> PRESS 'q'          
    ''')


def main():
    escolha = escolhamodo()

    if escolha['more_info']:
        instrucoes()

    elif escolha['json']:
        limites = json.load(open("limits.json"))

        cap = cv2.VideoCapture(0)
        name = 'AR_Paint'
        cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)

        text = 'Azul'
        while True:
            # c = readchar.readkey()
            _, frame = cap.read()

            # vai buscar os valore dos limites
            lim_inf = np.array([int(limites['B']['min']), int(limites['G']['min']), int(limites['R']['min'])])
            lim_sup = np.array([int(limites['B']['max']), int(limites['G']['max']), int(limites['R']['max'])])

            # aplica o limites e cria uma mascara
            mask = cv2.inRange(frame, lim_inf, lim_sup)

            # encotra o bloco maior

            _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            if len(contours) != 0:
                global tela, ponto_ini
                c = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(c)

                X_cm = x + w / 2
                Y_cm = y + h / 2

                # cv2.circle(frame,(X_cm,Y_cm),10,(0,255,0), -1)

                cv2.line(tela, (X_cm, Y_cm), (ponto_ini[0], ponto_ini[1]), (255, 0, 0), 10)
                ponto_ini = (X_cm, Y_cm)

            cv2.imshow('tela', tela)
            cv2.putText(frame, text, (40, 40), 1, 3, (255, 255, 255))
            cv2.imshow(name, frame)
            cv2.imshow('ff', mask)
            c = cv2.waitKey(1)

            # Criar mask onde se pinta

            if c == 114:  # Prime 'r' para riscar red
                text = 'red'
                print ('red')
                del c

            elif c == 103:  # Prime 'g' para riscar green
                print ('green')
                del c

            elif c == 98:  # Prime 'b' para riscar blue
                print ('blue')
                del c

            elif c == 43:  # Prime '+' para aumentar largura de risco
                print ('larger')
                del c

            elif c == 45:  # Prime '-' para diminuir largura de risco
                print ('thinner')
                del c

            elif c == 99:  # Prime 'c' para limpar a tela
                print ('clear')
                del c

            elif c == 119:  # Prime 'w' para guardar sketch
                print ('save')
                del c

            elif c == 113:  # Prime 'q' para sair
                cv2.destroyAllWindows()
                break
    else:
        instrucoes()


if __name__ == '__main__':
    main()
