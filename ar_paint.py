#!/usr/bin/env python

import argparse
import readchar
import cv2
import json
import numpy as np

def escolhamodo():
    parser = argparse.ArgumentParser(description="PARI AR Paint")
    parser.add_argument('-js' , '--json' , help = "Full path to json file" , action="store_true")
    parser.add_argument('-info' , '--more_info' , help = "List of commands", action="store_true")
    args = vars(parser.parse_args())
    return args

def instrucoes():
    print("!! PARI AR Paint !!")
    print("Here's some commands:")
    print("- QUIT          -> PRESS 'q'")
    print("- CLEAR         -> PRESS 'c'")
    print("- SAVE          -> PRESS 'w'")
    print("- RED PAINT     -> PRESS 'r'")
    print("- GREEN PAINT   -> PRESS 'g'")
    print("- BLUE PAINT    -> PRESS 'b'")
    print("- THICKER BRUSH -> PRESS '+'")
    print("- THINNER BRUSH -> PRESS '-'")

def main():
    escolha = escolhamodo()

    if escolha['more_info']:
        instrucoes()

    elif escolha['json']:
        #limites = json.load(open("limits.json"))

        cap = cv2.VideoCapture(0)
        name= 'AR_Paint'
        cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)

        while True:
            #c = readchar.readkey()
            _,frame = cap.read()
            cv2.imshow(name,frame)
            c = cv2.waitKey(1)

            # Criar mask onde se pinta

            if c == 114:        # Prime 'r' para riscar red
                print ('red')
                del c

            elif c == 103:      # Prime 'g' para riscar green
                print ('green')
                del c

            elif c == 98:       # Prime 'b' para riscar blue
                print ('blue')
                del c

            elif c == 43:       # Prime '+' para aumentar largura de risco
                print ('larger')
                del c

            elif c == 45:       # Prime '-' para diminuir largura de risco
                print ('thinner')
                del c

            elif c == 99:       # Prime 'c' para limpar a tela
                print ('clear')
                del c

            elif c == 119:       # Prime 'w' para guardar sketch
                print ('save')
                del c

            elif c == 113:       # Prime 'q' para sair
                cv2.destroyAllWindows()
                break
    else:
        instrucoes()




if __name__ == '__main__':
    main()