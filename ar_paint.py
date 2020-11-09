#!/usr/bin/env python
from colorama import Fore,Back,Style
import argparse
import cv2
import json
import numpy as np
import datetime
from time import ctime

# variaveis globais
ponto_ini = [0, 0]
color=(255,0,0)
raio=10





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
    # lista de instrucoes
    start = "\033[1m"
    end = "\033[0;0m"
    print('''
    -------------------------
    !!  AR_PAINT COMMAND LIST !!
    -------------------------''')
    print("- TO QUIT       "+u"\U000026D4"+"   -> PRESS 'q'")
    print("- TO CLEAR           -> PRESS 'c'")
    print("- TO SAVE       "+u"\U0001f4be"+"   -> PRESS 'w'")
    print("- RED PAINT   " + Back.RED + "      "+ Style.RESET_ALL +" -> PRESS "+ Fore.RED+"'r'"+Fore.RESET )
    print("- GREEN PAINT " + Back.GREEN + "      "+ Style.RESET_ALL +" -> PRESS "+ Fore.GREEN+"'g'"+Fore.RESET )
    print("- BLUE PAINT  " + Back.BLUE + "      "+ Style.RESET_ALL +" -> PRESS "+ Fore.BLUE+"'b'"+Fore.RESET )
    print(start + "- THICKER BRUSH "+ u"\U0001F58C"+ end + "    -> PRESS '"+start+"+"+end+"'")
    print("- THINNER BRUSH "+ u"\U0001F58C"+"    -> PRESS '-'")
    print("if u wanna see this tab again, just press 'H'")


def contornos(mask, frame, tela , tela_preta):

    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:



        c = max(contours, key=cv2.contourArea)
        area=cv2.contourArea(c)

        if area>300:


            x, y, w, h = cv2.boundingRect(c)

            #centroide
            X_cm = x + w / 2
            Y_cm = y + h / 2

            cv2.circle(frame, (X_cm, Y_cm), 10, (0, 255, 0), -1)

            global  ponto_ini



            cv2.line(tela, (X_cm, Y_cm), (ponto_ini[0], ponto_ini[1]), color, raio)
            cv2.line(tela_preta, (X_cm, Y_cm), (ponto_ini[0], ponto_ini[1]), color, raio)
            ponto_ini = (X_cm, Y_cm)

            aux = cv2.line(tela_preta, (X_cm, Y_cm), (ponto_ini[0], ponto_ini[1]), color, raio)
            gray_tela_preta = cv2.cvtColor(aux, cv2.COLOR_BGR2GRAY)
            _, th = cv2.threshold(gray_tela_preta, 10, 255, cv2.THRESH_BINARY)
            invert_th = cv2.bitwise_not(th)
            fr = cv2.bitwise_and(frame, frame, mask=invert_th)
            fr = cv2.add(fr, aux)


            return fr




        else:
            text_aviso='aproxime da camara o objeto'
            cv2.putText(frame, text_aviso, (40, 440), 1, 1, (255, 255, 255))
            fr=frame
            return fr

    else:
        fr=frame
        return fr











def main():
    escolha = escolhamodo()

    if escolha['more_info']:
        instrucoes()

    elif escolha['json']:
        limites = json.load(open("limits.json"))

        cap = cv2.VideoCapture(0)
        name = 'AR_Paint'
        cv2.namedWindow(name, cv2.WINDOW_AUTOSIZE)

        tela=None
        tela_preta=None

        text = 'Azul'
        while True:
            global color, raio
            _, frame = cap.read()

            if tela is None: tela = np.ones(frame.shape, dtype=np.uint8)*255
            if tela_preta is None: tela_preta = np.zeros(frame.shape, dtype=np.uint8)

            # vai buscar os valore dos limites
            lim_inf = np.array([int(limites['B']['min']), int(limites['G']['min']), int(limites['R']['min'])])
            lim_sup = np.array([int(limites['B']['max']), int(limites['G']['max']), int(limites['R']['max'])])


            # aplica o limites e cria uma mascara
            mask_orige = cv2.inRange(frame, lim_inf, lim_sup)

            filtro = np.ones((3, 3), np.uint8)
            mask = cv2.morphologyEx(mask_orige, cv2.MORPH_OPEN, filtro)
            #mask= cv2.morphologyEx(mask, cv2.MORPH_CLOSE,filtro)

            # encotra o bloco maior
            fr=contornos(mask,frame,tela, tela_preta)


            cv2.imshow('wwww',fr)
            cv2.imshow('tela', tela)
            cv2.imshow('telaP', tela_preta)
            cv2.putText(frame, text, (40, 40), 1, 3, color)
            cv2.imshow(name, frame)
            cv2.imshow('ff', mask)
            c = cv2.waitKey(1)

            # Criar mask onde se pinta

            if c == 114:  # Prime 'r' para riscar red
                text = 'red'
                color=(0,0,255)
                del c

            elif c == 103:  # Prime 'g' para riscar green
                text= 'green'
                color=(0,255,0)
                del c

            elif c == 98:  # Prime 'b' para riscar blue
                text='blue'
                color=(255,0,0)
                del c

            elif c == 43:  # Prime '+' para aumentar largura de risco
                raio+=1
                del c

            elif c == 45:  # Prime '-' para diminuir largura de risco
                if raio>1:
                    raio-=1
                del c

            elif c == 99:  # Prime 'c' para limpar a tela
                tela = np.ones([500, 500, 3], 'uint8') * 255
                del c

            elif c == 119:  # Prime 'w' para guardar sketch
                x = datetime.datetime.today()
                cv2.imwrite( 'drawing_'+x.strftime("%a_%b_%d_%H:%M:%S_%Y")+'.png', tela)
                del c

            elif c == 113:  # Prime 'q' para sair
                cv2.destroyAllWindows()
                break
    else:
        instrucoes()


if __name__ == '__main__':
    main()
