#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import numpy as np
import pygame
pygame.mixer.init()

def play_music(value):
    '''
    Falta ser definido o tipo de som, e testar outra biblioteca que não o pygame.
    Deveria ser um piano aberto, com a entrada de cada som, como se o mouse estivesse correndo sobre o teclado.
    O Pygame inicializa toda vez, e fica dando "tack, tack" para cada posição.
    '''
    frequency = value * 1000.
    sample_rate = 44100.
    duration_in_samples = 5 * sample_rate
    pygame.mixer.stop()
#    sound = pygame.mixer.Sound(np.array([math.sin(2.0 * math.pi * frequency * t / sample_rate) for t in xrange(0, duration_in_samples)]))
    
#   sound=pygame.mixer.Sound(np.array([(np.pi*frequency*t/sample_rate) for t in xrange(0,duration_in_sample)]))

    sound = pygame.mixer.Sound(np.array(frequency,dtype=np.float64))

    sound.play(loops=-1)

def main():
    def on_move(event):
        x,y = event.xdata, event.ydata
        print('x = %s & y = %s' % (x,y))
        if matriz.shape[1] > matriz.shape[0]: 
            play_music(matriz[y,x])
        else:
            play_music(matriz[x,y])
    pygame.mixer.stop()

    # Identificando os pontos
    #matriz = np.array([[15,14,13,12],[14,12,10,8],[13,10,7,4],[12,8,4,0]], dtype=np.float64)
    matriz = np.array([[15,14,13,12,11,7,9,5,13,11,12,18],[14,12,10,8,11,13,15,5,11,17,18,9],[13,10,7,4,11,17,8,9,18,11,14,11],[12,8,4,0,11,16,7,13,9,10,12,15]], dtype=np.float64)

    fig = plt.figure()
    fig.canvas.mpl_connect('motion_notify_event', on_move)
    ax = fig.add_subplot(111)
    ax.contourf(matriz)
    plt.show()

main()
