#!/usr/bin/env python

import cv2
import argparse
import json
import numpy as np


def escolhamodo():
    # funcao para escolher os modos
    esc_modo = argparse.ArgumentParser(description="escolha para o ficheiro JSON")
    esc_modo.add_argument('-j', '--json', help="Abre os valores escritos no ficheiro json", action="store_true")
    arg_list=vars(esc_modo.parse_args())
    return arg_list['json']


def main():

    if escolhamodo():
        limites= json.load(open("limits.json"))

    else:
        limites=dict(G={'max': 128, 'min': 128},
                              R={'max': 128, 'min': 128},
                              B={'max': 128, 'min': 128})












if __name__ == '__main__':
    main()